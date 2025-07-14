```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [filter, setFilter] = useState('');
  const [newCustomer, setNewCustomer] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const addCustomer = () => {
    if (newCustomer.trim()) {
      setCustomers([...customers, { name: newCustomer }]);
      setNewCustomer('');
    }
  };

  const filteredCustomers = customers.filter(customer => 
    customer.name.toLowerCase().includes(filter.toLowerCase())
  );

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Filter customers..." 
        value={filter} 
        onChange={e => setFilter(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index}>{customer.name}</li>
        ))}
      </ul>
      <input 
        type="text" 
        placeholder="New customer name" 
        value={newCustomer} 
        onChange={e => setNewCustomer(e.target.value)} 
      />
      <button onClick={addCustomer}>Add Customer</button>
    </div>
  );
};

export default CustomerManagement;
```