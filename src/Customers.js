```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch initial customers
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = async () => {
    const response = await fetch('/api/customers', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(newCustomer),
    });
    const newCust = await response.json();
    setCustomers([...customers, newCust]);
    setNewCustomer({ name: '', email: '' });
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        placeholder="Search Customers"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
      />
      <div>
        {filteredCustomers.map(customer => (
          <div key={customer.id}>
            <p>{customer.name} - {customer.email}</p>
          </div>
        ))}
      </div>
      <div>
        <input
          type="text"
          value={newCustomer.name}
          onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })}
          placeholder="Name"
        />
        <input
          type="email"
          value={newCustomer.email}
          onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })}
          placeholder="Email"
        />
        <button onClick={addCustomer}>Add Customer</button>
      </div>
    </div>
  );
};

export default CustomerManagement;
```