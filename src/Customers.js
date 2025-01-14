```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const addCustomer = () => {
    const newCustomer = { id: Date.now(), name, email };
    setCustomers([...customers, newCustomer]);
    setName('');
    setEmail('');
  };

  const removeCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
  };

  useEffect(() => {
    const initialCustomers = [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ];
    setCustomers(initialCustomers);
  }, []);

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Name" 
        value={name} 
        onChange={(e) => setName(e.target.value)} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={(e) => setEmail(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} ({customer.email}) 
            <button onClick={() => removeCustomer(customer.id)}>Remove</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManager;
```