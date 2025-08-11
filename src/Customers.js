```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchCustomers = () => {
      // Fetch customers from an API (mocked here)
      const fetchedCustomers = [
        { id: 1, name: 'John Doe', email: 'john@example.com' },
        { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
      ];
      setCustomers(fetchedCustomers);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    if (newCustomer.name && newCustomer.email) {
      setCustomers([...customers, { id: customers.length + 1, ...newCustomer }]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h2>Customer Management</h2>
      <input
        type="text"
        placeholder="Filter by name"
        value={filter}
        onChange={e => setFilter(e.target.value)}
      />
      <div>
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
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```