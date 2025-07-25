```javascript
import React, { useState } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const addCustomer = () => {
    if (name && email) {
      setCustomers([...customers, { id: customers.length + 1, name, email }]);
      setName('');
      setEmail('');
    }
  };

  const deleteCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Customer Name" />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Customer Email" />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} - {customer.email} <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```