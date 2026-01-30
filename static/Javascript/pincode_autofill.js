document.addEventListener("DOMContentLoaded", function () {

  const pincodeInput = document.querySelector('input[name="pincode"]');
  const districtInput = document.querySelector('input[name="district"]');
  const locationSelect = document.querySelector('select[name="location"]');
  const stateSelect = document.querySelector('select[name="state"]');

  const latInput = document.getElementById("id_latitude");
  const lngInput = document.getElementById("id_longitude");

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

  // ✅ PINCODE → district/state/areas autofill
  pincodeInput.addEventListener("input", function () {
    const pincode = this.value.trim();
    if (pincode.length !== 6) return;

    fetch(`https://api.postalpincode.in/pincode/${pincode}`)
      .then(res => res.json())
      .then(data => {
        if (data[0].Status !== "Success") return;

        const postOffices = data[0].PostOffice;
        const firstPO = postOffices[0];

        // ✅ Auto-fill district
        if (districtInput) districtInput.value = firstPO.District;

        // ✅ Auto-select state
        const stateCode = stateMap[firstPO.State];
        if (stateCode && stateSelect) {
          stateSelect.value = stateCode;
        }

        // ✅ Fill area dropdown
        if (locationSelect) {
          locationSelect.innerHTML = '<option value="">Select area</option>';

          postOffices.forEach(po => {
            const option = document.createElement("option");
            option.value = po.Name;
            option.textContent = `${po.Name}, ${po.Block}`;
            locationSelect.appendChild(option);
          });
        }
      })
      .catch(() => {
        console.log("Pincode fetch error");
      });
  });

  // ✅ lat/lng → pincode autofill (Map based)
  function fetchAddressFromLatLng(lat, lng) {
    fetch(`https://nominatim.openstreetmap.org/reverse?format=json&lat=${lat}&lon=${lng}&addressdetails=1`)
      .then(res => res.json())
      .then(data => {
        const address = data.address || {};

        if (address.postcode) {
          pincodeInput.value = address.postcode;

          // ✅ Trigger autofill of district/state/areas
          pincodeInput.dispatchEvent(new Event("input"));
        }
      })
      .catch(() => {
        console.log("Reverse geocode error");
      });
  }

  // ✅ Detect when lat/lng changes (after map auto-location or click)
  function watchLatLngAndFill() {
    if (!latInput || !lngInput) return;

    const lat = latInput.value;
    const lng = lngInput.value;

    if (lat && lng) {
      fetchAddressFromLatLng(lat, lng);
    }
  }

  // ✅ Run once after short delay (auto-location fills in async)
  setTimeout(watchLatLngAndFill, 1500);

});
