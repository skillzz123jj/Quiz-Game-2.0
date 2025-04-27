'use strict';

export async function fetchCountryData(country) {

  const response = await fetch(`http://localhost:5000/api/country?name=${encodeURIComponent(country)}`);

  if (!response.ok) {
    console.error("Failed to fetch data from the backend.");
    return;
  }
  const data = await response.json();
  console.log(data);
}


