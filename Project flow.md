# ☕ Software Engineering Final Project: "The Brew-Time" System

## 1. Project Overview

- **Project Title:** The Brew-Time (Smart Coffee Ordering System)
    
- **Target:** Alexandria National University - Faculty of Computer and Information
    
- **Core Objective:** To solve the problem of long queues and manual ordering errors in campus coffee shops using a digital ordering and status tracking system.
    

---

## 2. SDLC Phase 1: Requirements Phase

### 2.1 Problem Statement

Manual ordering systems lead to slow service, human error in orders, and lack of real-time updates for customers regarding their order status.

### 2.2 System Scope

The system will allow customers to browse products and place orders, while providing staff with a dashboard to manage the queue and update order statuses.

### 2.3 Functional Requirements (FR)

**FR1:** The system shall display a digital menu with prices.

**FR2:** Customers shall be able to add items to a cart and "Place Order."

**FR3:** The system shall generate a unique Order ID for every transaction.

**FR4:** Staff shall be able to view a list of active orders.

**FR5:** Staff shall be able to update order status (Pending → Preparing → Ready).

### 2.4 Non-Functional Requirements (NFR)

- **Performance:** The system should update the Barista dashboard within 2 seconds of an order being placed.
    
- **Usability:** The UI must be simple enough for a user to complete an order in under 4 clicks.
    
- **Reliability:** The system should maintain the order queue even if the browser is refreshed.
    

---

## 3. SDLC Phase 2: Design Phase (UML Planning)

As per project requirements, these diagrams must be computerized (use Draw.io or LucidChart).

### 3.1 Required UML Diagrams

1. **Use Case Diagram:**
    
    - **Actors:** Customer, Barista.
        
    - **Actions:** View Menu, Place Order, Login (Customer); View Orders, Update Status (Barista).
        
2. **Class Diagram:**
    
    - **Classes:** User, Product (ID, Name, Price), Order (OrderID, Status, Timestamp), OrderItem.
        
3. **Sequence Diagram:**
    
    - **Flow:** Customer → selects Item → clicks Checkout → System validates → Database saves → Barista Dashboard refreshes.
        
4. **Activity Diagram:**
    
    - **Flow:** Start → Browse Menu → Select Item → Pay? (Yes/No) → Confirm Order → Wait for Status → Receive Coffee → End.
        
5. **State Machine Diagram (Critical):**
    
    - **States of "Order" Object:** Placed ➔ In Preparation ➔ Ready for Pickup ➔ Completed.
        

---

## 4. SDLC Phase 3: Implementation Phase

### 4.1 Recommended Tech Stack (Easy & Fast)

- **Frontend:** HTML5, CSS3 (Bootstrap for styling), JavaScript.
    
- **Backend:** Python with Flask (Very beginner-friendly) OR Node.js.
    
- **Database:** SQLite (A simple file-based database, no installation needed).
    

### 4.2 Key Components

- app.py: The main logic for handling routes.
    
- templates/: Folder for HTML pages (index.html, barista.html).
    
- models.py: Database structure for Orders and Products.
    

---

## 5. SDLC Phase 4: Testing Phase

### 5.1 Testing Strategies

- **Unit Testing:** Testing the calculate_total() function to ensure it sums items correctly.
    
- **Integration Testing:** Ensuring the Customer's "Submit" action triggers an entry in the Barista's database.
    
- **System Testing:** A full "End-to-End" test: Order a Latte → Prepare it → Mark as Ready → Verify it disappears from the active queue.
    

### 5.2 Example Test Case

|   |   |   |   |
|---|---|---|---|
|Test ID|Description|Input|Expected Output|
|TC-01|Place Order|Click "Order" on 1 Latte|Database creates Order #101 with status 'Pending'|
|TC-02|Status Change|Barista clicks "Ready"|Customer UI shows "Your order is ready"|

---

## 6. SDLC Phase 5: Maintenance Phase

### 6.1 Future Improvements

- **Scalability:** Move from SQLite to PostgreSQL for handling thousands of daily orders.
    
- **Features:** Integrate a payment gateway (Stripe/PayPal) and customer loyalty points.
    
- **Updates:** Add a "Sales Report" feature for the shop owner to see daily revenue.
    

---

## 7. Presentation & Demonstration Flow

1. **Introduction:** State the problem (long coffee lines).
    
2. **Design Proof:** Show your UML diagrams first (proves you followed SE principles).
    
3. **The "Happy Path" Demo:**
    
    - Open **Window A** (Customer UI): Pick a coffee, click order.
        
    - Open **Window B** (Barista UI): Show the order appearing instantly.
        
    - **The Magic Moment:** Change the status in Window B and show Window A updating automatically.
        
4. **Conclusion:** Show a snippet of your testing report to prove it’s "Fully Functional."
    

---

## 📋 Final Submission Checklist

**Working Software:** Code zip file or GitHub link.

**Project Report:** PDF format (Following the SDLC phases).

**UML Diagrams:** All 5 diagrams included in the report (Computerized).

**Cover Page:** Name, Team, Instructor, Date.