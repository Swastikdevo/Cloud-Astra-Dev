```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Replace this with API call to fetch customers
    setCustomers([
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ]);
  }, []);

  const addCustomer = () => {
    if (newCustomer.name && newCustomer.email) {
      setCustomers([...customers, { id: Date.now(), ...newCustomer }]);
      setNewCustomer({ name: '', email: '' });
    }
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Search customers"
        value={searchTerm}
        onChange={e => setSearchTerm(e.target.value)}
      />
      <div>
        <input
          type="text"
          placeholder="Customer Name"
          value={newCustomer.name}
          onChange={e => setNewCustomer({ ...newCustomer, name: e.target.value })}
        />
        <input
          type="email"
          placeholder="Customer Email"
          value={newCustomer.email}
          onChange={e => setNewCustomer({ ...newCustomer, email: e.target.value })}
        />
        <button onClick={addCustomer}>Add Customer</button>
      </div>
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```