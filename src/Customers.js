```javascript
import React, { useState } from 'react';

const CustomerForm = () => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });
  const [customers, setCustomers] = useState([]);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setCustomer({ ...customer, [name]: value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setCustomers([...customers, customer]);
    setCustomer({ name: '', email: '', phone: '' });
  };

  return (
    <div>
      <h2>Add Customer</h2>
      <form onSubmit={handleSubmit}>
        <input type='text' name='name' value={customer.name} onChange={handleChange} placeholder='Name' required />
        <input type='email' name='email' value={customer.email} onChange={handleChange} placeholder='Email' required />
        <input type='tel' name='phone' value={customer.phone} onChange={handleChange} placeholder='Phone' required />
        <button type='submit'>Add Customer</button>
      </form>
      <ul>
        {customers.map((cust, index) => (
          <li key={index}>{cust.name} - {cust.email} - {cust.phone}</li>
        ))}
      </ul>
    </div>
  );
};

export default CustomerForm;
```