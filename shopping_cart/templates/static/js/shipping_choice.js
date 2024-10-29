const itellaRadio = document.getElementById('shipping-itella');
const omnivaRadio = document.getElementById('shipping-omniva');
const dpdRadio = document.getElementById('shipping-dpd');

const itellaContainer = document.getElementById('itella-container');
const omnivaContainer = document.getElementById('omniva-container');
const dpdContainer = document.getElementById('dpd-container');

const totalCart = document.getElementById('total-cart-price');
const shippingPriceContainer = document.getElementById('shipping-price-container');
const totalPriceContainer = document.getElementById('total-price-container');

let itellaPrice = 5;
let omnivaPrice = 10;
let dpdPrice = 15;

// default values
itellaRadio.checked = false;
omnivaRadio.checked = true;
itellaContainer.style.display = 'none';
omnivaContainer.style.display = 'block';
dpdContainer.style.display = 'none';
shippingPriceContainer.innerText = omnivaPrice;
calcTotal(totalCart, shippingPriceContainer);


itellaRadio.addEventListener('change', () => {
  if (itellaRadio.checked) {
    itellaContainer.style.display = 'block';
    omnivaContainer.style.display = 'none';
    dpdContainer.style.display = 'none';
    shippingPriceContainer.innerText = itellaPrice;
    calcTotal(totalCart, shippingPriceContainer);
  }
});

omnivaRadio.addEventListener('change', () => {
  if (omnivaRadio.checked) {
    itellaContainer.style.display = 'none';
    omnivaContainer.style.display = 'block';
    dpdContainer.style.display = 'none';
    shippingPriceContainer.innerText = omnivaPrice;
    calcTotal(totalCart, shippingPriceContainer);
  }
});

dpdRadio.addEventListener('change', () => {
  if (dpdRadio.checked) {
    itellaContainer.style.display = 'none';
    omnivaContainer.style.display = 'none';
    dpdContainer.style.display = 'block';
    shippingPriceContainer.innerText = dpdPrice;
    calcTotal(totalCart, shippingPriceContainer);
  }
});

function calcTotal(cart, shipping) {
  total = parseFloat(cart.innerText ) + parseFloat(shipping.innerText);
  return totalPriceContainer.innerText = total;
}