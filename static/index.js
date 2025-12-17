const form = document.getElementById("wishForm");
const wishesContainer = document.getElementById("wishes");

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const name = form.elements.name.value;
  const wish = form.elements.wish.value;
  const color = form.elements.color.value;

  await fetch("/wishes", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ name, wish, color }),
  });

  await loadWishes();
  form.reset();
});

async function loadWishes() {
  const response = await fetch("/wishes");
  const wishes = await response.json();

  wishesContainer.innerHTML = "";
  wishes.forEach((wish) => {
    const item = document.createElement("p");
    item.innerText = `${wish.name} wishes for ${wish.wish}`;
    item.style.color = wish.color;
    wishesContainer.appendChild(item);
  });
}

loadWishes();
