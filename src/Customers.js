```javascript
import React, { useState } from 'react';

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [filter, setFilter] = useState('');

  const addCustomer = () => {
    if (name && email) {
      setCustomers([...customers, { id: Date.now(), name, email }]);
      setName('');
      setEmail('');
    }
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type='text' 
        placeholder='Name' 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type='email' 
        placeholder='Email' 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <input 
        type='text' 
        placeholder='Search...' 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManager;
```