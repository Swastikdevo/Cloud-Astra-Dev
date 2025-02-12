```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const initialCustomers = [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ];
    setCustomers(initialCustomers);
  }, []);

  const addCustomer = () => {
    if (name && email) {
      setCustomers([...customers, { id: customers.length + 1, name, email }]);
      setName('');
      setEmail('');
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
        placeholder="Name" 
        value={name} 
        onChange={e => setName(e.target.value)} 
      />
      <input 
        type="email" 
        placeholder="Email" 
        value={email} 
        onChange={e => setEmail(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <input 
        type="text" 
        placeholder="Filter by name" 
        value={filter} 
        onChange={e => setFilter(e.target.value)} 
      />
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