document.addEventListener("DOMContentLoaded", async function () {
  try {
    const data = await getAllSpells();
    insertData(data, false);
  } catch (error) {
    console.error("Error:", error);
  }
});

