```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');
  const [filterTerm, setFilterTerm] = useState('');

  useEffect(() => {
    // Simulated fetch
    const fetchCustomers = () => {
      setCustomers(['Alice', 'Bob', 'Charlie', 'David']);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    if (newCustomer) {
      setCustomers([...customers, newCustomer]);
      setNewCustomer('');
    }
  };

  const filteredCustomers = customers.filter(customer =>
    customer.toLowerCase().includes(filterTerm.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={e => setNewCustomer(e.target.value)} 
        placeholder="Add New Customer" 
      />
      <button onClick={addCustomer}>Add</button>
      <input 
        type="text" 
        value={filterTerm} 
        onChange={e => setFilterTerm(e.target.value)} 
        placeholder="Search Customers" 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```