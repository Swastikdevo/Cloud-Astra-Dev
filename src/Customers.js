```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
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

  const deleteCustomer = (index) => {
    const newCustomers = customers.filter((_, idx) => idx !== index);
    setCustomers(newCustomers);
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        placeholder="Customer Name"
        value={customerName}
        onChange={(e) => setCustomerName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Customer Email"
        value={customerEmail}
        onChange={(e) => setCustomerEmail(e.target.value)}
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```