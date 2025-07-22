```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [filter, setFilter] = useState('');

  const addCustomer = () => {
    setCustomers([...customers, { name, email }]);
    setName('');
    setEmail('');
  };

  const filteredCustomers = customers.filter(customer => customer.name.includes(filter));

  return (
    <div>
      <h1>Customer Management System</h1>
      <input
        type="text"
        placeholder="Customer Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Customer Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <button onClick={addCustomer}>Add Customer</button>
      <input
        type="text"
        placeholder="Filter Customers"
        value={filter}
        onChange={(e) => setFilter(e.target.value)}
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