
-- change database and user
\connect datalake datalakeuser

-- Cria tabela de filmes
CREATE TABLE app.filmes (
    id_filme serial PRIMARY KEY,
    nome text,
    categoria text,
    censura text,
    atores_principais text,
    duracao time,
    produtora text,
    nacional boolean,
	descricao text NULL
);

-- Mock
INSERT INTO app.filmes VALUES (
    1, 'Eurotrip', 'comedia', '16', 'Michael Cera, etc', '01:50:00',
    'MGM', false, 'Um filme muito alto astral sobre amigos viajando na europa'
);

INSERT INTO app.filmes VALUES (
	6,'Racionais: Das Ruas de São Paulo pro Mundo','Documentário',14,'Mano Brown, Ice Blue, Edi Rock, KL Jay','01:56:00','NETFLIX',true,'Gravado ao longo de trinta anos, o documentário do Racionais MCs segue o grupo mais influente do rap nacional, desde sua criação. Mostrando a origem e ascensão do grupo, o documentário traz imagens inéditas de Mano Brown, KL Jay, Ice Blue e Edi Rock. Além de entrevistas, o documentário reforça o impacto e legado das músicas que introduziram o gênero no país, desde os primeiros shows de rap na ruas de São Paulo. Fundado em 1988, o nome do grupo é inspirado no álbum Tim Maia Racional e conseguiram lançar das músicas em uma coletânea, e anos depois apareceria no famoso álbum Holocausto Urbano, primeiro álbum do grupo que levantou temas como a violência e crime. Após o lançamento, o grupo tornou-se conhecido na cena do rap da periferia paulistana e da Grande SP. Seus trabalhos foram marcados por serem voltados para as comunidades pobres, além de projetos criados com a Secretaria Municipal de Educação de São Paulo.'
);

INSERT INTO app.filmes VALUES (
	3,'Adão Negro','Ação',12,'Dwayne Johnson, Aldis Hodge, Pierce Brosnan','02:05:00',' WARNER BROS',false,'Adão Negro é o filme solo do anti-herói, baseado no personagem em quadrinhos Black Adam (Dwayne Johnson) da DC Comics, grande antagonista de Shazam!, tendo no longa, sua história de origem explorada, e revelando seu passado de escravo no país Kahndaq. Nascido no Egito Antigo, o anti-herói tem super força, velocidade, resistência, capacidade de voar e de disparar raios. Alter ego de Teth-Adam e filho do faraó Ramsés II, Adão Negro foi consumido por poderes mágicos e transformado em um feiticeiro. Grande inimigo de Shazam! nas HQs, apesar dele acreditar em seu pontecial e, inclusive, oferecê-lo como um guerreiro do bem, Adão Negro acaba usando suas habilidades especiais para o mal. O anti-herói em busca de redenção ou um herói que se tornou vilão, pode ser capaz de destruir tudo o que estiver pela frente - ou de encontrar seu caminho. '
);

INSERT INTO app.filmes VALUES (
	2,'Sorria','Terror',14,'Sosie Bacon, Jessie T. Usher, etc','01:55:00',' PARAMOUNT PICTURES ',false,'Em Sorria, tudo na vida da Dra. Rose Cotter (Sosie Bacon) muda, após uma paciente morrer de forma brutal em sua frente, e ela testemunhar o incidente bizarro e traumático no consultório. A partir daí, ela começa a experimentar ocorrências assustadoras que ela não consegue explicar, mas que de alguma forma, se relacionam com a morte que ela presenciou. Para entender o fenômeno que não sai de sua cabeça, a Dra. irá atrás de respostas, mesmo que o mal também já esteja perseguindo-a, e tudo que ela mais quer, é também fugir. Rose irá até as últimas consequências, com o objetivo de desvendar e combater o mal desconhecido que começou a afetar sua vida e de todos ao seu redor. Cada dia mais imersa nessa teia de acontecimentos assustadores, para sobreviver, ela deverá enfrentar a situação perturbadora que se apresenta, e tentar escapar de sua nova e horrível realidade. '
);

INSERT INTO app.filmes VALUES (
	4,'Pantera Negra: Wakanda Para Sempre','Ação',12,'Letitia Wright, Angela Bassett, Danai Gurira','02:42:00','MARVEL',false,'Pantera Negra: Wakanda Para Sempre é a continuação do longa Pantera Negra, da Marvel, dirigido por Ryan Coogler e produzido por Kevin Feige. No filme, o mundo de Wakanda se expande. Após a morte do ator de TChalla (Chadwick Boseman) o foco de Wakanda Para Sempre são os personagens em volta do Pantera Negra. Rainha Ramonda (Angela Bassett), Shuri (Letitia Wright), MBaku (Winston Duke), Okoye (Danai Gurira) e as Dora Milage lutam para proteger a nação fragilizada de outros países após a morte de TChalla. Enquanto o povo de Wakanda se esforça para continuar em frente neste novo capítulo, a família e amigos do falecido rei precisam se unir com a ajuda de Nakia (Lupita Nyongo), integrante dos Cães de Guerra, e Everett Ross (Martin Freeman). Em meio a isso tudo, Wakanda ainda terá que aprender a conviver com a nação debaixo dágua, Talokan, e seu rei Namor (Tenoch Huerta). '
);

INSERT INTO app.filmes VALUES (
	5,'Marighella','Drama',16,'Seu Jorge, Adriana Esteves, Bruno Gagliasso','02:35:00',' PARIS FILMES ',true,'Neste filme biográfico, acompanhamos a história de Carlos Marighella, em 1969, um homem que não teve tempo pra ter medo. De um lado, uma violenta ditadura militar. Do outro, uma esquerda intimidada. Cercado por guerrilheiros 30 anos mais novos e dispostos a reagir, o líder revolucionário escolheu a ação. Marighella era político, escritor e guerrilheiro contra à ditadura militar brasileira. '
);
