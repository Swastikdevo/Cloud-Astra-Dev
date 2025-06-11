```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomerName, setNewCustomerName] = useState('');
  
  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);
  
  const addCustomer = () => {
    if (newCustomerName.trim()) {
      const newCustomer = { id: Date.now(), name: newCustomerName };
      setCustomers([...customers, newCustomer]);
      setNewCustomerName('');
      // Optionally post to API
    }
  };
  
  const deleteCustomer = (id) => {
    setCustomers(customers.filter(customer => customer.id !== id));
    // Optionally delete from API
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        value={newCustomerName} 
        onChange={(e) => setNewCustomerName(e.target.value)} 
        placeholder="New Customer Name" 
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map(customer => (
          <li key={customer.id}>
            {customer.name} <button onClick={() => deleteCustomer(customer.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```