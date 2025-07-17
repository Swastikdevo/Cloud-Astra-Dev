```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [inputName, setInputName] = useState('');
  const [inputEmail, setInputEmail] = useState('');

  useEffect(() => {
    const storedCustomers = JSON.parse(localStorage.getItem('customers')) || [];
    setCustomers(storedCustomers);
  }, []);

  const addCustomer = () => {
    const newCustomer = { name: inputName, email: inputEmail };
    const updatedCustomers = [...customers, newCustomer];
    setCustomers(updatedCustomers);
    localStorage.setItem('customers', JSON.stringify(updatedCustomers));
    setInputName('');
    setInputEmail('');
  };

  const deleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
    localStorage.setItem('customers', JSON.stringify(updatedCustomers));
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <input
        type="text"
        placeholder="Name"
        value={inputName}
        onChange={(e) => setInputName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={inputEmail}
        onChange={(e) => setInputEmail(e.target.value)}
      />
      <button onClick={addCustomer}>Add Customer</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {customer.name} - {customer.email}
            <button onClick={() => deleteCustomer(index)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerManagement;
```