import streamlit as st
from datetime import datetime, timedelta
import requests
import re

--- PAGE CONFIGURATION ---

st.set_page_config(page_title="Coffee with Chow", page_icon="☕", layout="centered")

--- INITIALIZE SHOPPING CART STATE ---

if 'cart' not in st.session_state:
st.session_state.cart = []
if 'ordered' not in st.session_state:
st.session_state.ordered = False

--- CONFIGURATION & BASE PRICES ---

PAYNOW_NUMBER = "9640 7262"
GOOGLE_SHEET_WEBAPP_URL = "google.com"
DRINK_PRICES = {
"Latte / White": {"Hot": 5.00, "Iced": 5.50},
"Mocha":         {"Hot": 5.50, "Iced": 6.00},
"Long Black":    {"Hot": 4.50, "Iced": 5.00}
}
def get_time_slots():
slots = []
current = datetime.strptime("09:00", "%H:%M")
end = datetime.strptime("12:00", "%H:%M")
while current <= end:
slots.append(current.strftime("%H:%M"))
current += timedelta(minutes=15)
return slots
TIME_SLOTS = get_time_slots()

--- MINIMALIST DESIGN SYSTEM (THIN BORDERS) ---

CSS_STYLE = """

.stApp {
padding: 8px !important;
}
.coffee-card {
background-color: #ffffff;
border: 1px solid #e5e7eb;
border-radius: 12px;
padding: 16px;
margin-bottom: 12px;
}
.cup-container {
display: flex;
justify-content: center;
align-items: center;
margin: 8px 0 16px 0;
}
.cup {
width: 64px;
height: 68px;
border: 1.5px solid #4a3424;
border-bottom-left-radius: 20px;
border-bottom-right-radius: 20px;
position: relative;
overflow: hidden;
background-color: transparent;
display: flex;
flex-direction: column-reverse;
}
.layer {
width: 100%;
text-align: center;
color: white;
font-size: 8px;
font-weight: 700;
display: flex;
align-items: center;
justify-content: center;
text-transform: uppercase;
letter-spacing: 0.5px;
}
.layer.espresso { background-color: #362215; height: 30%; }
.layer.milk { background-color: #ebdcb9; color: #4a3424; height: 50%; }
.layer.foam { background-color: #f7f3e9; color: #4a3424; height: 20%; }
.layer.chocolate { background-color: #1a0f07; height: 25%; }
.layer.water { background-color: #bce3eb; color: #1a3a40; height: 70%; }
.cup.latte .espresso { height: 30%; }
.cup.latte .milk { height: 55%; }
.cup.latte .foam { height: 15%; }
.cup.mocha .chocolate { height: 20%; }
.cup.mocha .espresso { height: 25%; }
.cup.mocha .milk { height: 45%; }
.cup.mocha .foam { height: 10%; }
.cup.longblack .water { height: 70%; }
.cup.longblack .espresso { height: 30%; }
h1 { font-size: 24px !important; font-weight: 800 !important; }
h2 { font-size: 18px !important; font-weight: 700 !important; }
h3 { font-size: 16px !important; font-weight: 700 !important; }

"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)
def validate_sg_phone(number):
clean_num = re.sub(r'\s+', '', number)
if re.match(r'^[89]\d{7}$', clean_num):
return clean_num
return None

--- STOREFRONT MENU ---

st.title("🏡 Coffee with Chow")
st.caption("📍 Punggol • Home Cafe Pickup")
st.markdown("---")
if not st.session_state.ordered:
st.subheader("📋 Menu Selection")
# --- DRINK 1: LATTE / WHITE ---
st.markdown('', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
st.markdown('EspressoMilkFoam', unsafe_allow_html=True)
with c2:
st.markdown("#### 1. Latte / White")
latte_temp = st.selectbox("Type", ["Iced", "Hot"], key="sel_latte_temp")
latte_oat = st.checkbox("🌾 Use Oat Milk (+$1.00)", key="chk_latte_oat")
base_p = DRINK_PRICES['Latte / White'][latte_temp]
unit_p = base_p + 1.00 if latte_oat else base_p
st.markdown(f"Price: ${unit_p:.2f}")
if st.button("🛒 Add Latte to Cart", key="btn_add_latte", use_container_width=True):
milk_tag = " (Oat Milk)" if latte_oat else ""
st.session_state.cart.append({
"item_name": f"{latte_temp} Latte / White{milk_tag}",
"price": unit_p
})
st.toast("Latte added to cart!", icon="☕")
st.markdown('', unsafe_allow_html=True)
# --- DRINK 2: MOCHA ---
st.markdown('', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
st.markdown('ChocEspressoMilkFoam', unsafe_allow_html=True)
with c2:
st.markdown("#### 2. Mocha")
mocha_temp = st.selectbox("Type", ["Iced", "Hot"], key="sel_mocha_temp")
mocha_oat = st.checkbox("🌾 Use Oat Milk (+$1.00)", key="chk_mocha_oat")
base_p = DRINK_PRICES['Mocha'][mocha_temp]
unit_p = base_p + 1.00 if mocha_oat else base_p
st.markdown(f"Price: ${unit_p:.2f}")
if st.button("🛒 Add Mocha to Cart", key="btn_add_mocha", use_container_width=True):
milk_tag = " (Oat Milk)" if mocha_oat else ""
st.session_state.cart.append({
"item_name": f"{mocha_temp} Mocha{milk_tag}",
"price": unit_p
})
st.toast("Mocha added to cart!", icon="🍫")
st.markdown('', unsafe_allow_html=True)
# --- DRINK 3: LONG BLACK ---
st.markdown('', unsafe_allow_html=True)
c1, c2 = st.columns(2)
with c1:
st.markdown('WaterEspresso', unsafe_allow_html=True)
with c2:
st.markdown("#### 3. Long Black")
lb_temp = st.selectbox("Type", ["Iced", "Hot"], key="sel_lb_temp")
lb_oat = st.checkbox("🌾 Add Oat Milk (+$1.00)", key="chk_lb_oat")
base_p = DRINK_PRICES['Long Black'][lb_temp]
unit_p = base_p + 1.00 if lb_oat else base_p
st.markdown(f"Price: ${unit_p:.2f}")
if st.button("🛒 Add Long Black to Cart", key="btn_add_lb", use_container_width=True):
milk_tag = " (Oat Milk)" if lb_oat else ""
st.session_state.cart.append({
"item_name": f"{lb_temp} Long Black{milk_tag}",
"price": unit_p
})
st.toast("Long Black added to cart!", icon="🖤")
st.markdown('', unsafe_allow_html=True)
# --- LOGISTICS & BILLING ---
st.markdown("---")
st.subheader("🕒 Collection Preferences")
selected_slot = st.selectbox("Select 15-Minute Pickup Window", TIME_SLOTS)
st.subheader("👤 Contact Details")
name = st.text_input("Your Name", placeholder="e.g. Rachel")
contact_input = st.text_input("WhatsApp Handphone Number", placeholder="e.g. 91234567")
valid_whatsapp = None
if contact_input:
valid_whatsapp = validate_sg_phone(contact_input)
if not valid_whatsapp:
st.error("🚨 Invalid Number: Please enter a valid 8-digit Singapore handphone number starting with 8 or 9.")
# --- SHOPPING BAG LEDGER ---
if st.session_state.cart:
st.markdown("---")
st.subheader("🛒 Current Shopping Bag")
grand_total = 0
items_summary = {}
for item in st.session_state.cart:
name_str = item["item_name"]
items_summary[name_str] = items_summary.get(name_str, 0) + 1
grand_total += item["price"]
for item_title, qty in items_summary.items():
st.write(f"- {qty}x {item_title}")
st.markdown(f"### Total Amount: ${grand_total:.2f}")
if st.button("❌ Clear Bag", use_container_width=True):
st.session_state.cart = []
st.rerun()
st.markdown("---")
if name and valid_whatsapp:
if st.button("Confirm Order & View PayNow Details", type="primary", use_container_width=True):
compiled_items = [f"{qty}x {item}" for item, qty in items_summary.items()]
query_params = {
"name": name,
"contact": valid_whatsapp,
"slot": selected_slot,
"items": ", ".join(compiled_items),
"total": f"${grand_total:.2f}"
}
try:
requests.get(GOOGLE_SHEET_WEBAPP_URL, params=query_params, timeout=10)
except Exception as e:
pass
st.session_state.customer_name = name
st.session_state.customer_contact = valid_whatsapp
st.session_state.customer_slot = selected_slot
st.session_state.grand_total = grand_total
st.session_state.ordered = True
st.rerun()
else:
st.info("💡 Please complete your Name and valid 8-digit WhatsApp Number above to open checkout.")
else:
st.info("Your shopping bag is empty. Select your options above and click 'Add to Cart'!")
else:
# --- FEE-FREE MOBILE PAYNOW SCREEN ---
st.balloons()
st.success("🎉 Pre-order Submitted Successfully!")
st.subheader(f"Next Steps for {st.session_state.customer_name}:")
st.write("1. Open your local banking app (DBS, OCBC, UOB, etc.)")
st.write("2. Select PayNow to Mobile Number and enter the details below:")
st.info(f"📱 Mobile Number: +65 {PAYNOW_NUMBER}\n\n💰 Exact Amount: ${st.session_state.grand_total:.2f}")
st.write("3. Send your payment transfer screenshot to the host immediately via WhatsApp to your number:")
st.code(st.session_state.customer_contact)
st.markdown("---")
st.subheader("🚨 Pickup & Collection Window")
st.markdown(f"⏰ Your Scheduled Time: Today between {st.session_state.customer_slot}")
st.caption("📍 Address Privacy: Once your transaction screenshot is verified via WhatsApp chat, your host will instantly send you the exact Punggol floor and unit number.")
if st.button("Back to Menu", use_container_width=True):
st.session_state.cart = []
st.session_state.ordered = False
st.rerun()
