import streamlit as st
from datetime import datetime, timedelta

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="Room 102 Coffee", page_icon="☕", layout="centered")

# --- INITIALIZE STATE ---
if 'ordered' not in st.session_state:
    st.session_state.ordered = False

# --- CONFIGURATION & BASE PRICES ---
PAYNOW_NUMBER = "9640 7262"
MAX_QTY = 3

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

# --- EXTERNAL STYLING SYSTEM ---
CSS_STYLE = """
<style>
    .coffee-card {
        background-color: #fcfcfc;
        border: 1px solid #eaeaea;
        border-radius: 12px;
        padding: 16px;
        margin-bottom: 20px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.02);
    }
    .cup-container {
        display: flex;
        justify-content: center;
        margin-bottom: 12px;
    }
    .cup {
        width: 70px;
        height: 75px;
        border: 4px solid #4a3424;
        border-bottom-left-radius: 24px;
        border-bottom-right-radius: 24px;
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
        font-weight: bold;
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
</style>
"""
st.markdown(CSS_STYLE, unsafe_allow_html=True)

# --- STOREFRONT INTERFACE ---
st.title("🏡 Room 102 Coffee")
st.caption("📍 Ang Mo Kio • Home Cafe Pickup")
st.markdown("---")

if not st.session_state.ordered:
    st.subheader("📋 Menu Selection")
    cart = {}

    # --- DRINK 1: LATTE / WHITE ---
    st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns()
    with col1:
        st.markdown('<div class="cup-container"><div class="cup latte"><div class="layer espresso">Espresso</div><div class="layer milk">Milk</div><div class="layer foam">Foam</div></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown("#### 1. Latte / White")
        st.caption("Rich espresso base with velvety smooth steamed milk.")
        latte_temp = st.selectbox("Temperature", ["Iced", "Hot"], key="latte_temp")
    with col3:
        st.markdown(f"<p style='text-align:right; font-weight:bold;'>\${DRINK_PRICES['Latte / White'][latte_temp]:.2f}</p>", unsafe_allow_html=True)
        latte_qty = st.selectbox("Quantity", list(range(MAX_QTY + 1)), key="latte_qty")
        if latte_qty > 0:
            cart[f"{latte_temp} Latte / White"] = {"qty": latte_qty, "unit_price": DRINK_PRICES['Latte / White'][latte_temp]}
    st.markdown('</div>', unsafe_allow_html=True)

    # --- DRINK 2: MOCHA ---
    st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns()
    with col1:
        st.markdown('<div class="cup-container"><div class="cup mocha"><div class="layer chocolate">Choc</div><div class="layer espresso">Espresso</div><div class="layer milk">Milk</div><div class="layer foam">Foam</div></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown("#### 2. Mocha")
        st.caption("Espresso blended with dark chocolate and creamy milk.")
        mocha_temp = st.selectbox("Temperature", ["Iced", "Hot"], key="mocha_temp")
    with col3:
        st.markdown(f"<p style='text-align:right; font-weight:bold;'>\${DRINK_PRICES['Mocha'][mocha_temp]:.2f}</p>", unsafe_allow_html=True)
        mocha_qty = st.selectbox("Quantity", list(range(MAX_QTY + 1)), key="mocha_qty")
        if mocha_qty > 0:
            cart[f"{mocha_temp} Mocha"] = {"qty": mocha_qty, "unit_price": DRINK_PRICES['Mocha'][mocha_temp]}
    st.markdown('</div>', unsafe_allow_html=True)

    # --- DRINK 3: LONG BLACK ---
    st.markdown('<div class="coffee-card">', unsafe_allow_html=True)
    col1, col2, col3 = st.columns()
    with col1:
        st.markdown('<div class="cup-container"><div class="cup longblack"><div class="layer water">Water</div><div class="layer espresso">Espresso</div></div></div>', unsafe_allow_html=True)
    with col2:
        st.markdown("#### 3. Long Black")
        st.caption("Double shot of pristine espresso pulled over fresh water.")
        lb_temp = st.selectbox("Temperature", ["Iced", "Hot"], key="lb_temp")
    with col3:
        st.markdown(f"<p style='text-align:right; font-weight:bold;'>\${DRINK_PRICES['Long Black'][lb_temp]:.2f}</p>", unsafe_allow_html=True)
        lb_qty = st.selectbox("Quantity", list(range(MAX_QTY + 1)), key="lb_qty")
        if lb_qty > 0:
            cart[f"{lb_temp} Long Black"] = {"qty": lb_qty, "unit_price": DRINK_PRICES['Long Black'][lb_temp]}
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LOGISTICS & UPCHARGES ---
    st.markdown("---")
    st.subheader("🕒 Collection Preferences")
    
    # Oat Milk Customization (Escaped dollar sign)
    oat_milk = st.checkbox("🌾 Add \$1 for oat milk (Applies to all milk drinks in cart)")
    
    # Time slot collection dropdown
    selected_slot = st.selectbox("Select 15-Minute Pickup Window", TIME_SLOTS)

    # Customer Contact Info
    st.subheader("👤 Contact Details")
    name = st.text_input("Your Name", placeholder="e.g. Rachel")
    contact = st.text_input("WhatsApp Number or Telegram Handle", placeholder="e.g. 9123 4567 / @rachel")

    # --- CALCULATE TOTAL & SUBMIT ---
    if cart and name and contact and selected_slot:
        st.markdown("### 🛒 Order Review")
        subtotal = 0
        oat_milk_total = 0
        
        for name_str, details in cart.items():
            item_cost = details["qty"] * details["unit_price"]
            subtotal += item_cost
            st.write(f"- {details['qty']}x {name_str}: **\${item_cost:.2f}**")
            
            if oat_milk and ("Latte" in name_str or "Mocha" in name_str):
                oat_milk_total += (details["qty"] * 1.00)
        
        if oat_milk_total > 0:
            st.write(f"- 🌾 Oat Milk Substitution Upgrade: **\${oat_milk_total:.2f}**")
            
        grand_total = subtotal + oat_milk_total
        st.markdown(f"### **Total Amount Due: \${grand_total:.2f}**")
        
        if st.button("Confirm Order & View PayNow Details", type="primary"):
            st.session_state.customer_name = name
            st.session_state.customer_contact = contact
            st.session_state.customer_slot = selected_slot
            st.session_state.grand_total = grand_total
            st.session_state.cart = cart
            st.session_state.ordered = True
            st.rerun()
    else:
        st.warning("Please add at least 1 drink to your cart and fill out your details to submit your pre-order.")

else:
    # --- FEE-FREE PAYNOW SCREEN ---
    st.balloons()
    st.success("🎉 Pre-order Submitted Successfully!")
    
    st.markdown(f"""
    ### Next Steps for **{st.session_state.customer_name}**:
    
    1. **Open your preferred banking app** (DBS digibank, OCBC Digital, UOB TMRW, etc.)
    2. Choose **PayNow to Mobile Number** and enter:
    """)
    
    st.info(f"📱 **Mobile Number:** `+65 {PAYNOW_NUMBER}`\n\n💰 **Exact Amount:** `${st.session_state.grand_total:.2f}`")
    
    st.markdown("""
    3. **Send your payment screenshot** to the host immediately via your provided contact handles:
    """)
    st.code(f"{st.session_state.customer_contact}")
    
    st.markdown(f"""
    ---
    ### 🚨 Collection Details:
    * **Scheduled Window:** Today between **{st.session_state.customer_slot}**
    * **Address Privacy:** Once your payment transfer screenshot is verified over chat, the exact HDB floor and unit number will be revealed to you instantly.
    """)
    
    if st.button("Back to Menu"):
        st.session_state.ordered = False
        st.rerun()
