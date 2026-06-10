let cargosParaVotar = ['Prefeito', 'Governador', 'Presidente'];
let cargosVotados = [];
let cargoAtual = '';
let numeroDigitado = '';
let votoBranco = false;
let candidatosDoCargo = [];
let eleitorAtual = { id: null, nome: '' }; // Identidade de quem está votando

// --- FLUXO DE TELAS ---
function mostrarTela(idTela) {
    document.querySelectorAll('body > div').forEach(div => div.style.display = 'none');
    document.getElementById(idTela).style.display = idTela === 'tela-urna' ? 'flex' : 'block';
}

function voltarAdmin() {
    carregarEleitores();
    mostrarTela('tela-admin');
}

// --- CRUD DE ELEITORES (MESÁRIO) ---
async function carregarEleitores() {
    let res = await fetch('/api/eleitores');
    let eleitores = await res.json();
    let tbody = document.getElementById('tabela-eleitores');
    tbody.innerHTML = '';

    eleitores.forEach(e => {
        tbody.innerHTML += `
            <tr>
                <td>${e.nome}</td>
                <td>
                    <button onclick="editarEleitor(${e.id}, '${e.nome}')">Editar</button>
                    <button onclick="deletarEleitor(${e.id})" style="color:red;">Deletar</button>
                    <button onclick="imprimirRelatorio(${e.id}, '${e.nome}')">Ver Votos</button>
                </td>
                <td>
                    <button onclick="liberarUrna(${e.id}, '${e.nome}')" style="background: green; color:white;">Liberar Urna</button>
                </td>
            </tr>
        `;
    });
}

async function adicionarEleitor() {
    let nome = document.getElementById('novo-eleitor').value;
    if(!nome) return alert("Digite um nome!");
    await fetch('/api/eleitores', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({nome}) });
    document.getElementById('novo-eleitor').value = '';
    carregarEleitores();
}

async function editarEleitor(id, nomeAntigo) {
    let novoNome = prompt("Novo nome:", nomeAntigo);
    if(novoNome && novoNome !== nomeAntigo) {
        await fetch(`/api/eleitores/${id}`, { method: 'PUT', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({nome: novoNome}) });
        carregarEleitores();
    }
}

async function deletarEleitor(id) {
    if(confirm("Deletar eleitor e todos os seus votos?")) {
        await fetch(`/api/eleitores/${id}`, { method: 'DELETE' });
        carregarEleitores();
    }
}

async function imprimirRelatorio(eleitorId = null, eleitorNome = '') {
    let url = eleitorId ? `/api/relatorio?eleitor_id=${eleitorId}` : '/api/relatorio';
    let res = await fetch(url);
    let relatorio = await res.json();

    document.getElementById('titulo-relatorio').innerText = eleitorId ? `Votos do Eleitor: ${eleitorNome}` : 'Total Geral de Votos';

    let tabelaHtml = '<table border="1" style="width:100%; border-collapse: collapse;"><tr><th>Cargo</th><th>Número</th><th>Nome</th>';
    tabelaHtml += eleitorId ? '</tr>' : '<th>Total de Votos</th></tr>';

    relatorio.forEach(r => {
        let nomeDisplay = r.nome ? r.nome : (r.tipo_voto === 'branco' ? 'Voto em Branco' : 'Voto Nulo');
        tabelaHtml += `<tr><td>${r.cargo}</td><td>${r.numero_candidato || '-'}</td><td>${nomeDisplay}</td>`;
        if(!eleitorId) tabelaHtml += `<td><b>${r.total_votos}</b></td>`;
        tabelaHtml += '</tr>';
    });
    tabelaHtml += '</table>';

    document.getElementById('tabela-relatorio').innerHTML = tabelaHtml;
    mostrarTela('tela-relatorio');
}

// --- FLUXO DA URNA ELETRÔNICA ---
function liberarUrna(id, nome) {
    eleitorAtual = { id, nome };
    cargosVotados = [];
    document.getElementById('nome-eleitor-atual').innerText = nome;
    ['Prefeito', 'Governador', 'Presidente'].forEach(cargo => document.getElementById(`btn-${cargo}`).disabled = false);
    mostrarTela('tela-menu');
}

async function iniciarVotacao(cargo) {
    cargoAtual = cargo;
    document.getElementById('cargo').innerText = cargo;
    document.getElementById('nome-cargo-lista').innerText = cargo;
    let res = await fetch(`/api/candidatos?cargo=${cargo}`);
    candidatosDoCargo = await res.json();
    prepararUrna();
    mostrarTela('tela-urna');
}

function prepararUrna() {
    numeroDigitado = ''; votoBranco = false;
    document.getElementById('descricao-candidato').innerHTML = '';
    document.getElementById('foto-candidato-container').innerHTML = '';
    document.getElementById('numeros').innerHTML = '<div class="numero-box pisca"></div><div class="numero-box"></div>';
    atualizarListaLateral();
}

function atualizarListaLateral() {
    let listaHtml = '';
    candidatosDoCargo.forEach(c => {
        if(c.numero.startsWith(numeroDigitado)) listaHtml += `<li><b>${c.numero}</b> - ${c.nome}</li>`;
    });
    document.getElementById('lista-candidatos').innerHTML = listaHtml;
}

function atualizarDisplay() {
    let boxes = document.querySelectorAll('.numero-box');
    for (let i = 0; i < boxes.length; i++) {
        boxes[i].innerText = numeroDigitado[i] || '';
        boxes[i].classList.remove('pisca');
        if (i === numeroDigitado.length) boxes[i].classList.add('pisca');
    }
    atualizarListaLateral();
    if (numeroDigitado.length === 2) {
        let cand = candidatosDoCargo.find(c => c.numero === numeroDigitado);
        if (cand) {
            document.getElementById('descricao-candidato').innerHTML = `Nome: <b>${cand.nome}</b><br>Partido: <b>${cand.partido}</b>`;
            document.getElementById('foto-candidato-container').innerHTML = `<img src="${cand.foto}" width="100" style="position:absolute; top:20px; right:20px;">`;
        } else {
            document.getElementById('descricao-candidato').innerHTML = '<div class="aviso-grande">VOTO NULO</div>';
        }
    }
}

function clicou(n) { if (!votoBranco && numeroDigitado.length < 2) { numeroDigitado += n; atualizarDisplay(); } }
function corrige() { prepararUrna(); }
function branco() { if (numeroDigitado === '') { votoBranco = true; document.getElementById('numeros').innerHTML = ''; document.getElementById('descricao-candidato').innerHTML = '<div class="aviso-grande">VOTO EM BRANCO</div>'; } }

async function confirma() {
    let tipoVoto = 'valido';
    let isNulo = document.getElementById('descricao-candidato').innerText.includes("NULO");
    if (votoBranco) tipoVoto = 'branco';
    else if (isNulo) tipoVoto = 'nulo';
    else if (numeroDigitado.length !== 2) return;

    // Envia o Voto associado ao Eleitor Atual
    await fetch('/api/votar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ eleitor_id: eleitorAtual.id, cargo: cargoAtual, numero: numeroDigitado, tipo: tipoVoto })
    });

   document.getElementById(`btn-${cargoAtual}`).disabled = true;
    cargosVotados.push(cargoAtual);

    if (cargosVotados.length === 3) {
        // Trava o eleitor no banco de dados para ele não conseguir votar de novo
        await fetch(`/api/eleitores/${eleitorAtual.id}/encerrar`, { method: 'POST' });

        alert("Sessão encerrada com sucesso!");
        voltarAdmin(); // Retorna ao mesário e atualiza a tela
    } else {
        mostrarTela('tela-menu');
    }
}

// Inicia o sistema carregando a tabela
async function carregarEleitores() {
    let res = await fetch('/api/eleitores');
    let eleitores = await res.json();
    let tbody = document.getElementById('tabela-eleitores');
    tbody.innerHTML = '';

    eleitores.forEach(e => {
        // A mágica acontece aqui: se ele já votou, o botão fica cinza e desativado
        let botaoUrna = e.ja_votou
            ? `<button disabled style="background: gray; color:white; padding: 10px; border: none; cursor: not-allowed; border-radius: 5px;">Já Votou</button>`
            : `<button onclick="liberarUrna(${e.id}, '${e.nome}')" style="background: green; color:white; padding: 10px; border: none; cursor: pointer; border-radius: 5px;">Liberar Urna</button>`;

        tbody.innerHTML += `
            <tr>
                <td style="padding: 10px;">${e.nome}</td>
                <td style="padding: 10px;">
                    <button class="btn-acao" onclick="editarEleitor(${e.id}, '${e.nome}')">Editar</button>
                    <button class="btn-acao" onclick="deletarEleitor(${e.id})" style="background:red;">Deletar</button>
                    <button class="btn-acao" onclick="imprimirRelatorio(${e.id}, '${e.nome}')">Ver Votos</button>
                </td>
                <td style="padding: 10px; text-align: center;">
                    ${botaoUrna}
                </td>
            </tr>
        `;
    });
}