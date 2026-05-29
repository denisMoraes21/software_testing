async function createUser() {

    const name = document.getElementById("create-name").value;

    const response = await fetch("/users/create", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name
        })
    });

    if (response.ok) {

        const data = await response.json();

        console.log("Usuário criado:", data);

        alert("Usuário criado com sucesso!");
    }
    else {
        alert("Erro ao criar usuário");
    }
}


async function deleteUser() {

    const id = document.getElementById("delete-id").value;

    const response = await fetch("/users/delete", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            id: Number(id)
        })
    });

    if (response.ok) {
        alert("Usuário deletado com sucesso!");
    }
    else {
        alert("Erro ao deletar usuário");
    }
}