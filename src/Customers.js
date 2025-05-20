```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');
  const [selectedCustomer, setSelectedCustomer] = useState(null);
  const [filter, setFilter] = useState('');

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleAddCustomer = () => {
    if (newCustomer) {
      const updatedCustomers = [...customers, { name: newCustomer }];
      setCustomers(updatedCustomers);
      setNewCustomer('');
    }
  };

  const handleSelectCustomer = (customer) => {
    setSelectedCustomer(customer);
  };

  const filteredCustomers = customers.filter(customer => customer.name.includes(filter));

  return (
    <div>
      <h1>Customer Management</h1>
      <input 
        type="text" 
        placeholder="Add new customer" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <input 
        type="text" 
        placeholder="Filter customers" 
        value={filter} 
        onChange={(e) => setFilter(e.target.value)} 
      />
      <ul>
        {filteredCustomers.map((customer, index) => (
          <li key={index} onClick={() => handleSelectCustomer(customer)}>
            {customer.name}
          </li>
        ))}
      </ul>
      {selectedCustomer && <h2>Selected Customer: {selectedCustomer.name}</h2>}
    </div>
  );
};

export default CustomerManagement;
```