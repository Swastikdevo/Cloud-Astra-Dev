```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');
  const [searchTerm, setSearchTerm] = useState('');

  useEffect(() => {
    // Fetch customers from an API or local storage
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    if (newCustomer) {
      setCustomers([...customers, { name: newCustomer }]);
      setNewCustomer('');
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
        value={newCustomer} 
        onChange={e => setNewCustomer(e.target.value)} 
        placeholder="Add new customer" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <input 
        type="text" 
        value={searchTerm} 
        onChange={e => setSearchTerm(e.target.value)} 
        placeholder="Search customers" 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```