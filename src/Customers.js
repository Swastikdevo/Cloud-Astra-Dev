```javascript
import React, { useState, useEffect } from 'react';

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');

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
      setCustomers([...customers, { name: newCustomer }]);
      setNewCustomer('');
    }
  };

  const handleDeleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
  };

  return (
    <div>
      <h3>Customer Management</h3>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={e => setNewCustomer(e.target.value)} 
        placeholder="Add new customer" 
      />
      <button onClick={handleAddCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name}
            <button onClick={() => handleDeleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManager;
```