```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchData();
  }, []);

  const addCustomer = () => {
    setCustomers([...customers, newCustomer]);
    setNewCustomer({ name: '', email: '' });
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Filter by name"
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <div>
        {filteredCustomers.map((customer, index) => (
          <div key={index}>
            <h3>{customer.name}</h3>
            <p>{customer.email}</p>
          </div>
        ))}
      </div>
      <input
        type="text"
        placeholder="Name"
        value={newCustomer.name}
        onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })}
      />
      <input
        type="email"
        placeholder="Email"
        value={newCustomer.email}
        onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })}
      />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```