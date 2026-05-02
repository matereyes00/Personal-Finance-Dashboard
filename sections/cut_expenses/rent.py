import streamlit as st
from datetime import date
from utils.conversion_rate import get_rates

def rent():
    rates = get_rates("AUD")
    php_rate = rates["PHP"]
   
    st.header("Rent")
    st.write("Rent takes up the largest share of my monthly expenses. I currently live at a student accomodation called Scape. It's honestly not the most affordable option, but I chose it for its convenience and the fact that it includes utilities and internet in the rent. However, I'm always on the lookout for more affordable housing options, especially as my lease is up for renewal soon.")
    st.write("529 per month for a single room in a shared apartment is quite expensive, but I value the convenience and the amenities that come with it. I'm considering looking for a cheaper place to live after my lease ends, but for now, I'm making it work by budgeting carefully and cutting down on other expenses.")
    col1, col2, col3 = st.columns(3)
    col1.metric("Current Rent (AUD) [PAID FORTNIGHTLY]", f"${529 * 2:,.2f}")
    rates = get_rates("AUD")
    ph_conversion_rate = rates["PHP"]

    fortnightly_rent_aud = 529 * 2
    yearly_rent_aud = fortnightly_rent_aud * 26
    yearly_rent_php = yearly_rent_aud * ph_conversion_rate
    col2.metric(
        "Rent (AUD) — Yearly",
        f"${yearly_rent_aud:,.2f}"
    )

    col3.metric(
        "Rent (PHP) — Yearly",
        f"₱{yearly_rent_php:,.2f}"
    )


    WEEKLY_RENT = 529
    LEASE_START = date(2026, 2, 6)
    LEASE_END = date(2027, 2, 5)
    FORTNIGHTLY_RENT = WEEKLY_RENT * 2
    TOTAL_FORTNIGHTS = 26

    TOTAL_LEASE_RENT_AUD = FORTNIGHTLY_RENT * TOTAL_FORTNIGHTS
    TOTAL_DAYS = (LEASE_END - LEASE_START).days

    st.subheader("📄 Lease Break Fee Simulator")

    break_lease = st.toggle("I am considering breaking my lease")

    if break_lease:
        break_date = st.date_input(
            "When would you break the lease?",
            min_value=LEASE_START,
            max_value=LEASE_END
        )

        elapsed_days = (break_date - LEASE_START).days
        progress = elapsed_days / TOTAL_DAYS

        if progress < 0.25:
            weeks = 4
        elif progress < 0.50:
            weeks = 3
        elif progress < 0.75:
            weeks = 2
        else:
            weeks = 1

        break_fee_aud = weeks * WEEKLY_RENT

        # Currency conversion
        break_fee_php = break_fee_aud * php_rate

        # rent already paid
        weeks_elapsed = elapsed_days / 7
        rent_paid_aud = weeks_elapsed * WEEKLY_RENT

        # total cost if breaking
        total_cost_if_break_aud = rent_paid_aud + break_fee_aud
        # net difference vs finishing lease
        loss_vs_finishing_aud = TOTAL_LEASE_RENT_AUD - total_cost_if_break_aud
        loss_vs_finishing_php = loss_vs_finishing_aud * php_rate
        

        st.subheader("💸 Estimated Break Fee")
        st.write(
            f"You are **{progress*100:.1f}%** through your lease.\n\n"
            f"Under Clause 28(a), your break fee would be:"
        )

        col1, col2, col3 = st.columns(3)
        col1.metric("Break Fee (AUD)", f"${break_fee_aud:,.2f}")
        col2.metric("Break Fee (PHP)", f"₱{break_fee_php:,.2f}")
        col3.metric(
            "Net difference vs finishing the lease (PHP)",
            f"₱{loss_vs_finishing_php:,.2f}"
        )
        col3.caption(" how much future rent you avoid paying by breaking early (after accounting for the break fee)")


        st.caption(
            "This estimate assumes a 12‑month fixed‑term lease starting 6 Feb 2026."
        )


    st.subheader("🪶Rent-saving alternatives")
    st.write("Roomshare or Houseshare: Sharing a house or apartment with roommates can significantly reduce your rent. You can split the cost of rent and utilities, making it more affordable than living alone. Look for shared housing options on websites like Flatmates.com.au or Gumtree.")


    '''
    variables for comparing rent
    - weekly rent 
    - bond
    '''

    # --- Inputs ---
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Current Place")
        current_weekly = st.number_input(
            "Weekly Rent (AUD)",
            min_value=0.0,
            step=10.0,
            key="current_weekly"
        )
        current_bond = st.number_input(
            "Bond (AUD)",
            min_value=0.0,
            step=100.0,
            key="current_bond"
        )
        current_utilities = st.checkbox(
            "Utilities included?",
            key="current_utilities"
        )

    with col2:
        st.markdown("### New Place")
        new_weekly = st.number_input(
            "Weekly Rent (AUD)",
            min_value=0.0,
            step=10.0,
            key="new_weekly"
        )
        new_bond = st.number_input(
            "Bond (AUD)",
            min_value=0.0,
            step=100.0,
            key="new_bond"
        )
        new_utilities = st.checkbox(
            "Utilities included?",
            key="new_utilities"
        )

    # --- Calculations ---
    if current_weekly > 0 and new_weekly > 0:
        WEEKS_PER_YEAR = 52

        yearly_current = current_weekly * WEEKS_PER_YEAR
        yearly_new = new_weekly * WEEKS_PER_YEAR

        yearly_diff = yearly_new - yearly_current
        savings_aud = abs(yearly_diff)
        savings_php = savings_aud * php_rate
        bond_diff = new_bond - current_bond

        st.divider()
        st.subheader("📊 Comparison Summary")

        colA, colB, colC = st.columns(3)

        
        weekly_diff = yearly_diff / WEEKS_PER_YEAR
        colA.metric(
            "Weekly Rent Change",
            f"${abs(weekly_diff):,.2f}",
            delta="Cheaper" if weekly_diff < 0 else "More expensive"
        )

        colB.metric(
            "Yearly Rent Change",
            f"${abs(yearly_diff):,.2f}",
            delta="You save per year" if yearly_diff < 0 else "Extra cost per year"
        )
        
        colC.metric(
            "Up‑front Bond Change",
            f"${abs(bond_diff):,.2f}",
            delta="Less upfront" if bond_diff < 0 else "More upfront"
        )

        # --- Interpretation ---
        if yearly_diff < 0:
            st.success(
                f"The new place saves you **${abs(yearly_diff):,.2f} "
                f"(₱{savings_php:,.2f}) per year** in rent."
            )
        elif yearly_diff > 0:
            extra_php = yearly_diff * php_rate
            st.warning(
                f"The new place costs **${yearly_diff:,.2f} "
                f"(₱{extra_php:,.2f}) more per year** in rent."
            )
        else:
            st.info("Both places cost the same per year.")


        # --- Utilities context ---
        if current_utilities != new_utilities:
            if new_utilities:
                st.info("Utilities are included in the new place — higher rent may be offset.")
            else:
                st.info("Utilities are not included in the new place — budget accordingly.")

    # rates = get_rates("AUD")
    # php_rate = rates["PHP"]

    # yearly_diff_php = yearly_diff * php_rate

    # st.metric(
    #     "Yearly Difference (PHP)",
    #     f"₱{yearly_diff_php:,.2f}"
    # )

'''
Suburbs to look into:
- Chippendale
- Pyrmont*
- Newtown
- Glebe*
- Redfern
- Surry Hills
- Ashfield
- Burwood*
'''