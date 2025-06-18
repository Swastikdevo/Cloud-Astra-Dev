```javascript
import React, { useState } from 'react';

const CustomerForm = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');

  const handleAddCustomer = () => {
    if (name && email) {
      setCustomers([...customers, { name, email }]);
      setName('');
      setEmail('');
    }
  };

  return (
    <div>
      <h2>Customer Management</h2>
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
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerForm;
```