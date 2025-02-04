```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Simulating fetching customers from an API
    const fetchCustomers = () => {
      const initialCustomers = [
        { id: 1, name: 'Alice', email: 'alice@example.com' },
        { id: 2, name: 'Bob', email: 'bob@example.com' }
      ];
      setCustomers(initialCustomers);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    const newCustomer = { id: Date.now(), name, email };
    setCustomers([...customers, newCustomer]);
    setName('');
    setEmail('');
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        placeholder="Search by name..." 
        value={searchTerm} 
        onChange={(e) => setSearchTerm(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map(customer => (
          <li key={customer.id}>{customer.name} - {customer.email}</li>
        ))}
      </ul>
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
    </div>
  );
};

export default CustomerManagement;
```