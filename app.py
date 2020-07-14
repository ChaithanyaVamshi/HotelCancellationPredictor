import streamlit as st
import pickle,bz2
import time
import numpy as np

pickle_in = bz2.BZ2File('modelfinal.pkl','rb')
model = pickle.load(pickle_in)

@st.cache(persist=True)
def predict_cancel(lead_time,adr,total_of_special_requests,booking_changes,market_segment,
deposit_type,assigned_room_type,customer_type,required_car_parking_spaces,previous_cancellations):
    input=np.array([[lead_time,adr,total_of_special_requests,booking_changes,market_segment,
    deposit_type,assigned_room_type,customer_type,required_car_parking_spaces,previous_cancellations]])
    prediction=model.predict_proba(input)
    pred='{0:.{1}f}'.format(prediction[0][0], 2)
    return float(pred)

def main():
    #st.markdown("## PREDICTING HOTEL BOOKING CANCELLATIONS")
    st.sidebar.header("Predicting Hotel Cancellations Using Machine Learning")
    st.sidebar.text("Choose the Below Parameters to Predict")
    st.sidebar.markdown("#### Lead Time")
    lead_time = st.sidebar.slider("Choose the Lead Time (Days)",0,400,step = 5)
    st.sidebar.markdown("#### Average Daily Rate (ADR)")
    adr = st.sidebar.slider("Choose the ADR", 0, 1000, step=25)
    st.sidebar.markdown("#### Total Special Requests")
    total_of_special_requests = st.sidebar.slider("Choose the number of special requests from guests", 0, 5, step=1)
    st.sidebar.markdown("#### Total Modifications")
    booking_changes = st.sidebar.slider("Choose the number of modifications made by guests", 0, 30, step=1)
    st.sidebar.markdown("#### Previous Cancellations By Guest")
    previous_cancellations = st.sidebar.slider("Choose the number of previous cancellations made by guests", 0, 30,step=1)
    st.sidebar.markdown("#### Market Segment")
    market_segment = st.sidebar.selectbox("Choose the Market Segment",[0,1,2,3,4,5,6,7])
    st.sidebar.info("0: Aviation, 1 : Complementary, 2: Corporate, 3: Direct, 4 : Groups, 5: Offline TA/TO, 6: Online TA,7: Undefined")
    st.sidebar.markdown("#### Deposit Type")
    deposit_type = st.sidebar.selectbox("Choose the Deposit Type",[0,1,2])
    st.sidebar.info("0 : No Deposit, 1 : Non Refund, 2 : Refundable")
    st.sidebar.markdown("#### Assigned Room Type")
    assigned_room_type = st.sidebar.selectbox("Choose the Assigned Room Type", [0,1,2,3,4,5,6,7,8,9,10,11])
    st.sidebar.info("0 : A, 1 : B, 2 : C, 3 : D, 4 : E, 5: F, 6 : G, 7 : H, 8 : I, 9 : K, 10 : L, 11 : P")
    st.sidebar.markdown("#### Customer Type")
    customer_type = st.sidebar.selectbox("Choose the Customer Type", [0,1,2,3])
    st.sidebar.info("0 : Contract, 1 : Group, 2 : Transient, 3 : Transient-Party ")
    st.sidebar.markdown("#### Car Parking")
    required_car_parking_spaces = st.sidebar.selectbox("Choose the number of Car Parking Spaces", [1,2,3,4,5,6,7,8])

    html_temp = """
        <div style="background-color:#000000 ;padding:10px">
        <h2 style="color:white;text-align:center;">Hotel Booking Cancellations Prediction ML App</h2>
        </div>
     """
    st.markdown(html_temp, unsafe_allow_html=True)

    safe_html = """ 
    <img src="https://media.giphy.com/media/g9582DNuQppxC/giphy.gif" alt="confirmed" style="width:698px;height:350px;"> 
    """

    danger_html = """  
    <img src="https://media.giphy.com/media/8ymvg6pl1Lzy0/giphy.gif" alt="cancel" style="width:698px;height:350px;">
    """

    hotelvideo_html = """
     <img src="https://media.giphy.com/media/f9SIUWTkLGOsQ9XaSX/giphy.gif" alt="success" style="width:698px;height:350px;">
    """
    st.markdown(hotelvideo_html, unsafe_allow_html=True)

    if st.button("Click Here To Predict"):
        output = predict_cancel(lead_time,adr,total_of_special_requests,booking_changes,market_segment,
        deposit_type,assigned_room_type,customer_type,required_car_parking_spaces,previous_cancellations)
        final_output = output * 100
        st.header('Probability of Guest Cancelling Reservation is {}% '.format(final_output))

        if final_output > 50.0:
            st.markdown(danger_html, unsafe_allow_html=True)
            st.error("OMG! Reservation is not confirmed")
        else:
            st.balloons()
            time.sleep(2)
            st.balloons()
            st.markdown(safe_html, unsafe_allow_html=True)
            st.success("Hurray! Reservation is confirmed")

if __name__=='__main__':
    main()
