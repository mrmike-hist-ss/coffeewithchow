import streamlit as st
from datetime import datetime, timedelta
import requests

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Coffee with Chow", page_icon="☕", layout="centered")

# --- INITIALIZE STATE ---
if 'ordered' not in st.session_state:
    st.session_state.ordered = False

# --- CONFIGURATION & BASE PRICES ---
PAYNOW_NUMBER = "9640 7262"
MAX_QTY = 3

# 🔗 Your verified Google Apps Script URL
GOOGLE_SHEET_WEBAPP_URL = "https://google.com"

DRINK_PRICES = {
    "Latte / White": {"Hot": 5.00, "Iced": 5.50},
    "Mocha":         {"Hot": 5.50, "Iced": 6.00},
    "Long Black":    {"Hot": 4.50, "Iced": 5.00}
}

# Generate 15-minute collection slots from 9:00 AM to 12:00 PM
def get_time_slots():
    slots = []
    current = datetime.strptime("09:00", "%H:%M")
    end = datetime.strptime("12:00", "%H:%M")
    while current <= end:
        slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=15)
    return slots

TIME_SLOTS = get_time_slots()

# --- MOBILE-FIRST CSS STYLING ---
CSS_STYLE = """
<style>
    .stApp {
        padding: 8px !important;
    }
    .coffee-card {
        background-color: #fafafa;
        border: 1px solid #e0e0e0;
        border-radius: 16px;
        padding: 16px;
        margin-bottom: 16px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02);
    }
    .cup-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 8px 0 16px 0;
    }
    .cup {
        width: 68px;
        height: 72px;
        border: 4px solid #4a3424;
        border-bottom-left-radius: 22px;
        border-bottom-right-radius: 22px;
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
        font-size: 9px;
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
    
    h1 { font-size: 26px !important; font-weight: 800 !important; }
    h2 { font-size: 20px !important; font-weight: 700 !important; }
    h3 { font-size: 18px !important; font-weight: 700 !important; }
    
    div[data-testid="stBlock"] {
        padding: 0px !important;
    }
</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- STOREFRONT INTERFACE ---
st.title("🏡 Coffee with Chow")
st.caption("📍 Punggol • Home Cafe Pickup")
st.markdown("---")

if not st.session_state.ordered:
    st.subheader("📋 Menu Selection")
    cart = {}

    # --- DRINK 1: LATTE / WHITE ---
    st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="cup-container"><div class="cup latte"><div class="layer espresso">Espresso</div><div class="layer milk">Milk</div><div class="layer foam">Foam</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown("#### 1. Latte / White")
        latte_temp = st.selectbox("Type", ["Iced", "Hot"], key="latte_temp", label_visibility="collapsed")
        latte_oat = st.checkbox("🌾 Use Oat Milk (+\$1.00)", key="latte_oat")
        
        base_p = DRINK_PRICES['Latte / White'][latte_temp]
        unit_p = base_p + 1.00 if latte_oat else base_p
        st.markdown(f"Price: **\${unit_p:.2f}**")
        
        latte_qty = st.selectbox("Quantity", list(range(MAX_QTY + 1)), key="latte_qty")
        if latte_qty > 0:
            milk_label = " (Oat Milk)" if latte_oat else ""
            cart[f"{latte_temp} Latte / White{milk_label}"] = {"qty": latte_qty, "unit_price": unit_p}
    st.markdown('</div>', unsafe_allow_html=True)

    # --- DRINK 2: MOCHA ---
    st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="cup-container"><div class="cup mocha"><div class="layer chocolate">Choc</div><div class="layer espresso">Espresso</div><div class="layer milk">Milk</div><div class="layer foam">Foam</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown("#### 2. Mocha")
        mocha_temp = st.selectbox("Type", ["Iced", "Hot"], key="mocha_temp", label_visibility="collapsed")
        mocha_oat = st.checkbox("🌾 Use Oat Milk (+\$1.00)", key="mocha_oat")
        
        base_p = DRINK_PRICES['Mocha'][mocha_temp]
        unit_p = base_p + 1.00 if mocha_oat else base_p
        st.markdown(f"Price: **\${unit_p:.2f}**")
        
        mocha_qty = st.selectbox("Quantity", list(range(MAX_QTY + 1)), key="mocha_qty")
        if mocha_qty > 0:
            milk_label = " (Oat Milk)" if mocha_oat else ""
            cart[f"{mocha_temp} Mocha{milk_label}"] = {"qty": mocha_qty, "unit_price": unit_p}
    st.markdown('</div>', unsafe_allow_html=True)

    # --- DRINK 3: LONG BLACK ---
    st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown('<div class="cup-container"><div class="cup longblack"><div class="layer water">Water</div><div class="layer espresso">Espresso</div></div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown("#### 3. Long Black")
        lb_temp = st.selectbox("Type", ["Iced", "Hot"], key="lb_temp", label_visibility="collapsed")
        lb_oat = st.checkbox("🌾 Add Oat Milk (+\$1.00)", key="lb_oat")
        
        base_p = DRINK_PRICES['Long Black'][lb_temp]
        unit_p = base_p + 1.00 if lb_oat else base_p
        st.markdown(f"Price: **\${unit_p:.2f}**")
        
        lb_qty = st.selectbox("Quantity", list(range(MAX_QTY + 1)), key="lb_qty")
        if lb_qty > 0:
            milk_label = " (Oat Milk)" if lb_oat else ""
            cart[f"{lb_temp} Long Black{milk_label}"] = {"qty": lb_qty, "unit_price": unit_p}
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LOGISTICS ---
    st.markdown("---")
    st.subheader("🕒 Collection Preferences")
    selected_slot = st.selectbox("Select 15-Minute Pickup Window", TIME_SLOTS)

    st.subheader("👤 Contact Details")
    name = st.text_input("Your Name", placeholder="e.g. Rachel")
    contact = st.text_input("WhatsApp Number / Telegram", placeholder="e.g. 9123 4567")

    # --- LIVE BREAKDOWN & VALIDATION ---
    if cart:
        st.markdown("---")
        st.markdown("### 🛒 Order Review")
        grand_total = 0
        items_list = []
        
        for name_str, details in cart.items():
            item_cost = details["qty"] * details["unit_price"]
            grand_total += item_cost
            items_list.append(f"{details['qty']}x {name_str}")
            st.write(f"- {details['qty']}x {name_str}: **\${item_cost:.2f}**")
            
        st.markdown(f"### **Total Amount Due: \${grand_total:.2f}**")
        
        if name and contact:
            if st.button("Confirm Order & View PayNow Details", type="primary", use_container_width=True):
                form_payload = {
                    "name": name,
                    "contact": contact,
                    "slot": selected_slot,
                    "items": ", ".join(items_list),
                    "total": f"\${grand_total:.2f}"
                }
                
                try:
                    requests.post(GOOGLE_SHEET_WEBAPP_URL, data=form_payload, timeout=10)
                except Exception as e:
                    pass

                st.session_state.customer_name = name
                st.session_state.customer_contact = contact
                st.session_state.customer_slot = selected_slot
                st.session_state.grand_total = grand_total
                st.session_state.cart = cart
                st.session_state.ordered = True
                st.rerun()
        else:
            st.info("💡 Please key in your Name and Contact Details above to open the checkout button.")
    else:
        st.warning("Please select a quantity for at least 1 coffee to start your order.")

else:
    # --- FEE-FREE MOBILE PAYNOW SCREEN ---
    st.balloons()
    st.success("🎉 Pre-order Submitted Successfully!")
    
    st.subheader(f"Next Steps for {st.session_state.customer_name}:")
    st.write("1. Open your banking app (DBS, OCBC, UOB, etc.)")
    st.write("2. Select PayNow to Mobile and enter details below:")
    
    st.info(f"📱 **Mobile Number:** `+65 {PAYNOW_NUMBER}`\n\n💰 **Exact Amount:** `${st.session_state.grand_total:.2f}`")
    
    st.write("3. **Send your payment screenshot** to the host immediately via your handle:")
    st.code(st.session_state.customer_contact)
    
    st.markdown("---")
    st.subheader("🚨 Pickup & Collection Window")
    st.markdown(f"⏰ **Your Scheduled Time:** Today between **{st.session_state.customer_slot}**")
    st.caption("📍 **Address Privacy:** Once your transaction screenshot is verified via chat, your host will instantly send you the exact floor and unit number.")
    
    if st.button("Back to Menu", use_container_width=True):
        st.session_state.ordered = False
        st.rerun()
