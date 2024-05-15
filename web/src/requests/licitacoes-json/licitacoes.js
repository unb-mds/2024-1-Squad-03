const requestURL = "https://raw.githubusercontent.com/Marcelo-Adrian/Diario-extractor/main/output.json"

// Função para fazer a requisição e processar os dados
async function fetchData() {
  try {
    const response = await fetch(requestURL);
    
    if (!response.ok) {
      throw new Error(`HTTP error! Status: ${response.status}`);
    }

    const data = await response.json();


    return data
  } catch (error) {

    console.error('Erro ao buscar os dados:', error);
    return -1
  }
}

const data = fetchData()

export default data