if (document.querySelector("#id_person_image") !== null) {
  document.querySelectorAll("main ul").forEach((e) => {
    e.style.height = `${e.scrollHeight}px`;
  });
  document.querySelector("#id_person_image").addEventListener("input", function () {
    document
      .querySelectorAll(".upload-label")[0]
      .querySelector("p").innerHTML = `File name : ${this.files[0].name}`;
  });
  document.querySelector("#id_passport_image").addEventListener("input", function () {
    document
      .querySelectorAll(".upload-label")[1]
      .querySelector("p").innerHTML = `File name : ${this.files[0].name}`;
  });
  document.querySelector("#id_person_id_image").addEventListener("input", function () {
    document
      .querySelectorAll(".upload-label")[2]
      .querySelector("p").innerHTML = `File name : ${this.files[0].name}`;
  });
  document.querySelector("#id_person_brd_image").addEventListener("input", function () {
    document
      .querySelectorAll(".upload-label")[3]
      .querySelector("p").innerHTML = `File name : ${this.files[0].name}`;
  });
  document.querySelector("#id_person_hotel_image").addEventListener("input", function () {
    document
      .querySelectorAll(".upload-label")[4]
      .querySelector("p").innerHTML = `File name : ${this.files[0].name}`;
  });
  document.querySelector("#id_person_flight_image").addEventListener("input", function () {
    document
      .querySelectorAll(".upload-label")[5]
      .querySelector("p").innerHTML = `File name : ${this.files[0].name}`;
  });
  document.querySelectorAll('input[name="russia"]').forEach((e) => {
    e.addEventListener("input", function () {
      if (
        document.querySelector('input[name="russia"]:checked').value === "no"
      ) {
        this.parentElement.parentElement.nextElementSibling.style.height =
          "0px";
        document.getElementById('russia_relative_stat').value = 'no'
      } else if (
        document.querySelector('input[name="russia"]:checked').value === "yes"
      ) {
        this.parentElement.parentElement.nextElementSibling.style.height = `${this.parentElement.parentElement.nextElementSibling.scrollHeight}px`;
        document.getElementById('russia_relative_stat').value = 'yes'
      }
    });
  });
  document.querySelectorAll('input[name="marial"]').forEach((e) => {
    e.addEventListener("input", function () {
      if (
        document.querySelector('input[name="marial"]:checked').value === "no"
      ) {
        this.parentElement.parentElement.nextElementSibling.style.height =
          "0px";
        document.getElementById('marial_stat').value = 'no'
      } else if (
        document.querySelector('input[name="marial"]:checked').value === "yes"
      ) {
        this.parentElement.parentElement.nextElementSibling.style.height = `${this.parentElement.parentElement.nextElementSibling.scrollHeight}px`;
        document.getElementById('marial_stat').value = 'yes'
      }
    });
  });
  document.querySelectorAll('input[name="gender"]').forEach((e) => {
    e.addEventListener("input", function () {
      if (
        document.querySelector('input[name="gender"]:checked').value === "male"
      ) {

        document.getElementById('gender_type').value = 'Male'
      } else if (
        document.querySelector('input[name="gender"]:checked').value === "female"
      ) {

        document.getElementById('gender_type').value = 'Female'
      }
    });
  });
  document.querySelectorAll('input[name="highschool"]').forEach((e) => {
    e.addEventListener("input", function () {
      if (
        document.querySelector('input[name="highschool"]:checked').value ===
        "no"
      ) {
        this.parentElement.parentElement.nextElementSibling.style.height =
          "0px";
        document.getElementById('uni_degree_stat').value = 'no'
      } else if (
        document.querySelector('input[name="highschool"]:checked').value ===
        "yes"
      ) {
        this.parentElement.parentElement.nextElementSibling.style.height = `${this.parentElement.parentElement.nextElementSibling.scrollHeight}px`;
        document.getElementById('uni_degree_stat').value = 'yes'
      }
    });
  });
}
