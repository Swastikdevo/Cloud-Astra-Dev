```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [searchTerm, setSearchTerm] = useState('');

  const fetchCustomers = async () => {
    // Simulating an API call
    const data = [
      { id: 1, name: 'John Doe', email: 'john@example.com' },
      { id: 2, name: 'Jane Smith', email: 'jane@example.com' },
    ];
    setCustomers(data);
  };

  useEffect(() => {
    fetchCustomers();
  }, []);

  const handleAddCustomer = () => {
    setCustomers((prev) => [...prev, { ...newCustomer, id: Date.now() }]);
    setNewCustomer({ name: '', email: '' });
  };

  const filteredCustomers = customers.filter(customer =>
    customer.name.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management System</h1>
      <input 
        type="text" 
        placeholder="Search Customers" 
        value={searchTerm} 
        onChange={(e) => setSearchTerm(e.target.value)} 
      />
      <div>
        <input 
          type="text" 
          placeholder="Name" 
          value={newCustomer.name} 
          onChange={(e) => setNewCustomer({ ...newCustomer, name: e.target.value })} 
        />
        <input 
          type="email" 
          placeholder="Email" 
          value={newCustomer.email} 
          onChange={(e) => setNewCustomer({ ...newCustomer, email: e.target.value })} 
        />
        <button onClick={handleAddCustomer}>Add Customer</button>
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