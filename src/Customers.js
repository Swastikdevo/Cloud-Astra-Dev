```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filteredCustomers, setFilteredCustomers] = useState([]);

  useEffect(() => {
    fetchCustomers();
  }, []);

  const fetchCustomers = async () => {
    const response = await fetch('/api/customers');
    const data = await response.json();
    setCustomers(data);
    setFilteredCustomers(data);
  };

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const addedCustomer = await response.json();
    setCustomers([...customers, addedCustomer]);
    setFilteredCustomers([...filteredCustomers, addedCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  const handleSearch = (e) => {
    const query = e.target.value.toLowerCase();
    setFilteredCustomers(customers.filter(customer => customer.name.toLowerCase().includes(query)));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Search customers"
        onChange={handleSearch}
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
      <input
        type="text"
        value={newCustomer.name}
        placeholder="Customer Name"
        onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })}
      />
      <input
        type="email"
        value={newCustomer.email}
        placeholder="Customer Email"
        onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })}
      />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```