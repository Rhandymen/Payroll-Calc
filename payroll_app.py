import streamlit as st

def format_currency(amount):
    return f"${amount:,.2f}"

def calculate_raise(base, raises, is_hourly=True):
    results = []
    current = base

    for i, raise_amt in enumerate(raises):
        new_pay = current + raise_amt
        percent = (raise_amt / current) * 100
        annual = new_pay * 2080 if is_hourly else new_pay
        results.append({
            "Year": f"Year {i+1}",
            "Old Pay": format_currency(current) + ("/hr" if is_hourly else "/yr"),
            "Raise": format_currency(raise_amt) + ("/hr" if is_hourly else "/yr"),
            "New Pay": format_currency(new_pay) + ("/hr" if is_hourly else "/yr"),
            "Annual Equivalent": format_currency(annual),
            "Percent Increase": f"{percent:.2f}%"
        })
        current = new_pay

    total_raise = sum(raises)
    total_percent = ((current - base) / base) * 100

    return results, total_raise, total_percent

# --- Streamlit App Layout ---
st.title("📈 B-Ville Raise Calculator")

pay_type = st.radio("Are you entering Hourly or Annual pay?", ["Hourly", "Annual"])
base = st.number_input(f"Enter Starting {'Hourly' if pay_type == 'Hourly' else 'Annual'} Pay", min_value=0.0, step=0.01)

raises = []
col1, col2, col3 = st.columns(3)
with col1:
    raise1 = st.number_input("Year 1 Raise", value=1.50 if pay_type == 'Hourly' else 1.50 * 2080, step=0.01)
with col2:
    raise2 = st.number_input("Year 2 Raise", value=2.00 if pay_type == 'Hourly' else 2.00 * 2080, step=0.01)
with col3:
    raise3 = st.number_input("Year 3 Raise", value=2.50 if pay_type == 'Hourly' else 2.50 * 2080, step=0.01)

raises = [raise1, raise2, raise3]

if st.button("Calculate Raise"):
    is_hourly = pay_type == "Hourly"
    results, total_raise, total_percent = calculate_raise(base, raises, is_hourly)

    st.subheader("📊 Raise Breakdown by Year")
    for row in results:
        st.markdown(f"**{row['Year']}**")
        st.write(f"• Original Pay: {row['Old Pay']}")
        st.write(f"• Raise: {row['Raise']}")
        st.write(f"• New Pay: {row['New Pay']}")
        st.write(f"• Annual Equivalent: {row['Annual Equivalent']}")
        st.write(f"• Percent Increase: {row['Percent Increase']}")
        st.markdown("---")

    st.subheader("📈 Total Summary")
    unit = "/hr" if is_hourly else "/yr"
    st.write(f"**Total Raise Over 3 Years:** {format_currency(total_raise)}{unit}")
    st.write(f"**Total Percent Increase:** {total_percent:.2f}%")
