```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState({ name: '', email: '' });
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch customers from API
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    if (newCustomer.name && newCustomer.email) {
      setCustomers([...customers, newCustomer]);
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
        placeholder="Search Customer" 
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
        {filteredCustomers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```