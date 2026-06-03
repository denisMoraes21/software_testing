let cargosParaVotar = ['Prefeito', 'Governador', 'Presidente'];
let cargosVotados = [];
let cargoAtual = '';
let numeroDigitado = '';
let votoBranco = false;
let candidatosDoCargo = [];

// Transição entre telas
function mostrarTela(idTela) {
    document.getElementById('tela-menu').style.display = 'none';
    document.getElementById('tela-urna').style.display = 'none';
    document.getElementById('tela-relatorio').style.display = 'none';
    document.getElementById(idTela).style.display = idTela === 'tela-urna' ? 'flex' : 'block';
}

// Inicia o voto para o cargo escolhido no menu
async function iniciarVotacao(cargo) {
    cargoAtual = cargo;
    document.getElementById('cargo').innerText = cargo;
    document.getElementById('nome-cargo-lista').innerText = cargo;
    
    // Busca os candidatos daquele cargo na API
    let res = await fetch(`/api/candidatos?cargo=${cargo}`);
    candidatosDoCargo = await res.json();
    
    prepararUrna();
    mostrarTela('tela-urna');
}

function prepararUrna() {
    numeroDigitado = '';
    votoBranco = false;
    document.getElementById('descricao-candidato').innerHTML = '';
    document.getElementById('foto-candidato-container').innerHTML = '';
    
    // Cria as caixinhas (2 dígitos para todos os cargos neste exemplo)
    document.getElementById('numeros').innerHTML = '<div class="numero-box pisca"></div><div class="numero-box"></div>';
    atualizarListaLateral();
}

function atualizarListaLateral() {
    let listaHtml = '';
    candidatosDoCargo.forEach(c => {
        // Filtra a lista conforme o número é digitado
        if(c.numero.startsWith(numeroDigitado)) {
            listaHtml += `<li><b>${c.numero}</b> - ${c.nome}</li>`;
        }
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
        buscarCandidato();
    }
}

function clicou(n) {
    if (votoBranco) return;
    if (numeroDigitado.length < 2) {
        numeroDigitado += n;
        atualizarDisplay();
    }
}

function branco() {
    if (numeroDigitado === '') {
        votoBranco = true;
        document.getElementById('numeros').innerHTML = '';
        document.getElementById('descricao-candidato').innerHTML = '<div class="aviso-grande">VOTO EM BRANCO</div>';
    }
}

function corrige() { prepararUrna(); }

async function buscarCandidato() {
    let cand = candidatosDoCargo.find(c => c.numero === numeroDigitado);
    if (cand) {
        document.getElementById('descricao-candidato').innerHTML = `Nome: <b>${cand.nome}</b><br>Partido: <b>${cand.partido}</b>`;
        document.getElementById('foto-candidato-container').innerHTML = `<img src="${cand.foto}" width="100" style="position:absolute; top:20px; right:20px;">`;
    } else {
        document.getElementById('descricao-candidato').innerHTML = '<div class="aviso-grande">VOTO NULO</div>';
    }
}

async function confirma() {
    let tipoVoto = 'valido';
    let isNulo = document.getElementById('descricao-candidato').innerText.includes("NULO");
    
    if (votoBranco) tipoVoto = 'branco';
    else if (isNulo) tipoVoto = 'nulo';
    else if (numeroDigitado.length !== 2) return; // Não confirma se não terminou de digitar

    // Registra o Voto via API (A mesma que você testará com o JMeter)
    await fetch('/api/votar', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ cargo: cargoAtual, numero: numeroDigitado, tipo: tipoVoto })
    });

    // Desativa o botão do cargo que acabou de ser votado
    document.getElementById(`btn-${cargoAtual}`).disabled = true;
    cargosVotados.push(cargoAtual);

    // Verifica se já votou nos 3
    if (cargosVotados.length === 3) {
        mostrarTela('tela-relatorio');
    } else {
        mostrarTela('tela-menu'); // Volta pro menu para escolher o próximo
    }
}

async function imprimirRelatorio() {
    let res = await fetch('/api/relatorio');
    let relatorio = await res.json();
    
    let tabelaHtml = '<table border="1" style="width:100%; margin-top:20px; border-collapse: collapse;"><tr><th>Cargo</th><th>Número/Tipo</th><th>Nome</th><th>Total de Votos</th></tr>';
    
    relatorio.forEach(r => {
        let nomeDisplay = r.nome ? r.nome : (r.tipo_voto === 'branco' ? 'Voto em Branco' : 'Voto Nulo');
        tabelaHtml += `<tr><td>${r.cargo}</td><td>${r.numero_candidato || '-'}</td><td>${nomeDisplay}</td><td><b>${r.total_votos}</b></td></tr>`;
    });
    tabelaHtml += '</table>';
    
    document.getElementById('tabela-relatorio').innerHTML = tabelaHtml;
}