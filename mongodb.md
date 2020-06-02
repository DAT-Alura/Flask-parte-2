use jogoteca

db.usuario.insertMany([
    { id: "daniel", nome: "Daniel Akio Teixeira", senha: "dat" },
    { id: "shodi", nome: "Henrique Shodi Maeta", senha: "hsm" },
    { id: "harikoi", nome: "Gabriel Lourenço Nicolini", senha: "gln" },
    { id: "matias", nome: "Matheus Pinto Teixeira", senha: "mpt" }
]);

db.jogo.insertMany([
    { nome: "God of War 4", categoria: "Acao", console: "PS4" },
    { nome: "NBA 2k18", categoria: "Esporte", console: "Xbox One" },
    { nome: "Rayman Legends", categoria: "Indie", console: "PS4" },
    { nome: "Super Mario RPG", categoria: "RPG", console: "SNES" },
    { nome: "Super Mario Kart", categoria: "Corrida", console: "SNES" },
    { nome: "Fire Emblem Echoes", categoria: "Estrategia", console: "3DS" }
]);