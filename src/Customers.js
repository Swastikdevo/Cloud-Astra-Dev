```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const addCustomer = () => {
    if (!name || !email) return;
    setCustomers([...customers, { name, email }]);
    setName('');
    setEmail('');
  };

  const handleDelete = (index) => {
    const newCustomers = customers.filter((_, i) => i !== index);
    setCustomers(newCustomers);
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Customer Name"
      />
      <input
        type="email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="Customer Email"
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => handleDelete(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```