```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [customerName, setCustomerName] = useState("");
  const [emailFilter, setEmailFilter] = useState("");

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    const newCustomer = { name: customerName, email: `${customerName}@example.com` };
    setCustomers([...customers, newCustomer]);
    setCustomerName("");
  };

  const filteredCustomers = customers.filter(customer => customer.email.includes(emailFilter));

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        value={customerName} 
        onChange={e => setCustomerName(e.target.value)} 
        placeholder="Add Customer Name" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <input 
        type="text" 
        value={emailFilter} 
        onChange={e => setEmailFilter(e.target.value)} 
        placeholder="Filter by Email" 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```