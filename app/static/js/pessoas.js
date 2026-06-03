async function createPessoa() {

    console.log("Botão clicado");

    const data = {

        nome_completo: document.getElementById(
            "nome_completo"
        ).value,

        cpf: document.getElementById(
            "cpf"
        ).value,

        data_nascimento: document.getElementById(
            "data_nascimento"
        ).value,

        sexo: document.getElementById(
            "sexo"
        ).value,

        estado_civil: document.getElementById(
            "estado_civil"
        ).value,

        nacionalidade: document.getElementById(
            "nacionalidade"
        ).value,

        telefone: document.getElementById(
            "telefone"
        ).value,

        celular: document.getElementById(
            "celular"
        ).value,

        email: document.getElementById(
            "email"
        ).value,

        cep: document.getElementById(
            "cep"
        ).value,

        logradouro: document.getElementById(
            "logradouro"
        ).value,

        numero: document.getElementById(
            "numero"
        ).value,

        complemento: document.getElementById(
            "complemento"
        ).value,

        bairro: document.getElementById(
            "bairro"
        ).value,

        cidade: document.getElementById(
            "cidade"
        ).value,

        estado: document.getElementById(
            "estado"
        ).value
    };

    console.log("Dados capturados:");
    console.log(data);

    try {

        console.log("Enviando requisição para o Flask...");

        const response = await fetch(
            "/pessoas/create",
            {
                method: "POST",

                headers: {
                    "Content-Type": "application/json"
                },

                body: JSON.stringify(data)
            }
        );

        console.log("Resposta recebida:");
        console.log(response);

        const result = await response.json();

        console.log("JSON retornado:");
        console.log(result);

        if (response.ok) {

            console.log("Cadastro realizado com sucesso");

            alert(
                "Pessoa cadastrada com sucesso!"
            );

        } else {

            console.log("Erro retornado pelo backend");

            alert(
                result.error
            );
        }

    } catch (error) {

        console.error(
            "Erro ao conectar com o servidor:"
        );

        console.error(error);

        alert(
            "Erro ao conectar com o servidor."
        );
    }
}