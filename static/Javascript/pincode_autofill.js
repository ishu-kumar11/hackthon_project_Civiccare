document.addEventListener("DOMContentLoaded", function () {

  const pincodeInput = document.querySelector('input[name="pincode"]');
  const districtInput = document.querySelector('input[name="district"]');
  const locationSelect = document.querySelector('select[name="location"]');
  const stateSelect = document.querySelector('select[name="state"]');

  if (!pincodeInput) return;

  const stateMap = {
    "Andhra Pradesh": "AP",
    "Arunachal Pradesh": "AR",
    "Assam": "AS",
    "Bihar": "BR",
    "Chhattisgarh": "CT",
    "Goa": "GA",
    "Gujarat": "GJ",
    "Haryana": "HR",
    "Himachal Pradesh": "HP",
    "Jharkhand": "JH",
    "Karnataka": "KA",
    "Kerala": "KL",
    "Madhya Pradesh": "MP",
    "Maharashtra": "MH",
    "Manipur": "MN",
    "Meghalaya": "ML",
    "Mizoram": "MZ",
    "Nagaland": "NL",
    "Odisha": "OR",
    "Punjab": "PB",
    "Rajasthan": "RJ",
    "Sikkim": "SK",
    "Tamil Nadu": "TN",
    "Telangana": "TG",
    "Tripura": "TR",
    "Uttar Pradesh": "UP",
    "Uttarakhand": "UT",
    "West Bengal": "WB",
    "Delhi": "DL",
    "Jammu and Kashmir": "JK",
    "Ladakh": "LA",
    "Puducherry": "PY",
    "Chandigarh": "CH",
    "Andaman and Nicobar Islands": "AN",
    "Dadra and Nagar Haveli and Daman and Diu": "DN",
    "Lakshadweep": "LD"
  };

  pincodeInput.addEventListener("keyup", function () {
    const pincode = this.value.trim();
    if (pincode.length !== 6) return;

    fetch(`https://api.postalpincode.in/pincode/${pincode}`)
      .then(res => res.json())
      .then(data => {
        if (data[0].Status !== "Success") return;

        const postOffices = data[0].PostOffice;
        const firstPO = postOffices[0];

        // ✅ Auto-fill district
        districtInput.value = firstPO.District;

        // ✅ Auto-select state
        const stateCode = stateMap[firstPO.State];
        if (stateCode) {
          stateSelect.value = stateCode;
        }

        // ✅ Fill area dropdown
        locationSelect.innerHTML = '<option value="">Select area</option>';

        postOffices.forEach(po => {
          const option = document.createElement("option");
          option.value = po.Name;
          option.textContent = `${po.Name}, ${po.Block}`;
          locationSelect.appendChild(option);
        });
      })
      .catch(() => {
        console.log("Pincode fetch error");
      });
  });

});
