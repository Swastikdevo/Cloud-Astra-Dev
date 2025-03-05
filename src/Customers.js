```javascript
import React, { useState } from 'react';

function CustomerManagement() {
  const [customers, setCustomers] = useState([]);
  const [customerName, setCustomerName] = useState('');
  const [customerEmail, setCustomerEmail] = useState('');

  const addCustomer = () => {
    if (customerName && customerEmail) {
      setCustomers([...customers, { name: customerName, email: customerEmail }]);
      setCustomerName('');
      setCustomerEmail('');
    }
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        value={customerName} 
        onChange={(e) => setCustomerName(e.target.value)} 
        placeholder="Customer Name" 
      />
      <input 
        type="email" 
        value={customerEmail} 
        onChange={(e) => setCustomerEmail(e.target.value)} 
        placeholder="Customer Email" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
}

export default CustomerManagement;
```