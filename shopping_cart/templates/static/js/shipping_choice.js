const itellaRadio = document.getElementById('shipping-itella');
const omnivaRadio = document.getElementById('shipping-omniva');
const dpdRadio = document.getElementById('shipping-dpd');
const addressRadio = document.getElementById('shipping-address');

const itellaContainer = document.getElementById('itella-container');
const omnivaContainer = document.getElementById('omniva-container');
const dpdContainer = document.getElementById('dpd-container');
const addressContainer = document.getElementById('address-container');

itellaRadio.checked = false;
omnivaRadio.checked = true;
itellaContainer.style.display = 'none';
omnivaContainer.style.display = 'block';
dpdContainer.style.display = 'none';
addressContainer.style.display = 'none';

itellaRadio.addEventListener('change', () => {
  if (itellaRadio.checked) {
    itellaContainer.style.display = 'block';
    omnivaContainer.style.display = 'none';
    dpdContainer.style.display = 'none';
    addressContainer.style.display = 'none';
  }
});

omnivaRadio.addEventListener('change', () => {
  if (omnivaRadio.checked) {
    itellaContainer.style.display = 'none';
    omnivaContainer.style.display = 'block';
    dpdContainer.style.display = 'none';
    addressContainer.style.display = 'none';
  }
});

dpdRadio.addEventListener('change', () => {
  if (dpdRadio.checked) {
    itellaContainer.style.display = 'none';
    omnivaContainer.style.display = 'none';
    dpdContainer.style.display = 'block';
    addressContainer.style.display = 'none';
  }
});

addressRadio.addEventListener('change', () => {
  if (addressRadio.checked) {
    itellaContainer.style.display = 'none';
    omnivaContainer.style.display = 'none';
    dpdContainer.style.display = 'none';
    addressContainer.style.display = 'block';
  }
});


dpdContainer.innerHTML = '<p>Work in Progress</p>';