import streamlit as st
from utils.conversion_rate import get_rates
from config import IMG_SIZE, LOGO_SIZE

def cheap_alternatives():
    st.write("This is where I will share some of the cheap alternatives that I have found to be useful in managing my expenses as an international student. I will be sharing some of the tips and tricks that I have learned along the way, as well as some of the resources that I have found to be helpful in finding discounts and deals on groceries, transportation, and other expenses. I hope that by sharing this information, I can help other students who are in a similar situation to find ways to save money and manage their finances more effectively.")
    st.write("Everything in Australia is generally more expensive in the Philippines. When I first arrived, I always compared the price of items in Australia to the price of the same item in the Philippines. I was shocked at how much more expensive things were here. For example, a loaf of bread that costs around \\$1 in the Philippines can cost around \\$3 here. A liter of milk that costs around \\$0.50 in the Philippines can cost around \\$1.50 here. Instead of comparing to PH prices all the time, I'd compare prices locally.")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(
                "https://s.yimg.com/ny/api/res/1.2/6LvCHmI58LUoQ7WV1J7Brg--/YXBwaWQ9aGlnaGxhbmRlcjt3PTk2MDtoPTg1OTtjZj13ZWJw/https://s.yimg.com/os/creatr-uploaded-images/2023-06/181ae0a0-0430-11ee-baff-c1cfc571d317",
                width=IMG_SIZE, 
            )
    with col2:
        st.image(
                "https://imageresizer.static9.net.au/JR8vJcDiW7c08UF8hnqvNrv7UL8=/1200x900/https%3A%2F%2Fprod.static9.net.au%2Ffs%2F1bcc5aa3-971d-4031-a826-a363c948e4de",
                width=IMG_SIZE, 
            )
    with col3:
        st.image(
                "https://content.api.news/v3/images/bin/ac4a2507f708827006cc4e8cf236966e",
                width=IMG_SIZE, 
            )
        
    st.write("For example, I'd always be on the lookout for discounts that are called 'everyday low prices' in the supermarket, or something similar to that. They're usually at the bottom of the shelf or tagged with a bright yellow label. I try to shop more at night, for the prices are marked down lower than the day, just because they want to get rid of those items. I also try to buy in bulk whenever there are discounts, especially for non-perishable items. I also try to buy store brands instead of name brands, as they are usually cheaper and of similar quality.")
    st.write("A more tiring, but effective, way I save is to compare prices of items in different supermarkets. I have a few supermarkets near me, and I try to check the prices of items in each supermarket before I buy them. This is especially helpful for items that are not on discount, as the price difference can be significant. I also try to use price comparison websites and apps to find the cheapest prices for items I need to buy.")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(
                "https://www.aldiunpacked.com.au/storage/2022/11/170403-ALDI-Australia-Brand-Logo-Landscape-1024x409.png",
                width=LOGO_SIZE, 
            )
    with col2:
        st.image(
                "https://www.glenrosevillage.com.au/wp-content/uploads/2017/03/woolworths-logo.png",
                width=LOGO_SIZE, 
            )
    with col3:
        st.image(
                "https://logos-world.net/wp-content/uploads/2022/04/Coles-Supermarkets-Logo-1991.png",
                width=LOGO_SIZE, 
            )

    store1_aud = st.text_input("Store 1 (AUD)")
    store2_aud = st.text_input("Store 2 (AUD)")

    if store1_aud and store2_aud:
        try:
            # Convert inputs safely
            price1 = float(store1_aud)
            price2 = float(store2_aud)

            # Determine savings
            higher_price = max(price1, price2)
            lower_price = min(price1, price2)
            saved_aud = higher_price - lower_price

            # Fetch conversion rate
            rates = get_rates("AUD")
            ph_conversion_rate = rates["PHP"]

            # Convert amounts
            store1_php = price1 * ph_conversion_rate
            store2_php = price2 * ph_conversion_rate
            saved_php = saved_aud * ph_conversion_rate

            # Display results
            st.write(f"**AUD → PHP rate:** {ph_conversion_rate:.2f}")
            st.write(f"Store 1: ₱{store1_php:,.2f}")
            st.write(f"Store 2: ₱{store2_php:,.2f}")

            st.success(
                f"You save **AUD ${saved_aud:,.2f}** "
                f"(≈ ₱{saved_php:,.2f}) by choosing the cheaper store!"
            )

        except ValueError:
            st.error("Please enter valid numeric prices (e.g. 12.50).")
        except Exception:
            st.error("Unable to fetch currency rates right now.")