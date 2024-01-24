function SendData(dataToSend) {
  // console.log("sent");
  fetch("http://127.0.0.1:8000/findSpellByName", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(dataToSend),
  })
    .then((response) => response.json())
    .then((data) => {
      console.log("Отримано від сервера:", data);
    })
    .catch((error) => {
      console.error("Помилка відправлення:", error);
    });
}


async function getAllSpells() {
  // console.log("sent");
  const backendUrl = "http://127.0.0.1:8000/spells";
  try {
    const response = await axios.get(backendUrl);
    return response.data;
  } catch (error) {
    console.error("Помилка при отриманні даних:", error.message);
    throw error;
  }
}


async function getSpellDescription() {
  // console.log("sent");
  const backendUrl = "http://127.0.0.1:8000/returnSpellsToTable/";
  try {
    const response = await axios.get(backendUrl);
    return response.data;
  } catch (error) {
    console.error("Помилка при отриманні даних:", error.message);
    throw error;
  }
}


// Example usage
// (async () => {
//   try {
      
//     const jsonData = await getData("http://127.0.0.1:8000/test");
//   } catch (error) {
//     console.error("Error:", error.message);
//   }
// })();