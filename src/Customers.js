```javascript
import React, { useState } from 'react';

const CustomerForm = () => {
  const [customer, setCustomer] = useState({ name: '', email: '', phone: '' });
  const [customers, setCustomers] = useState([]);

  const handleChange = (e) => {
    setCustomer({ ...customer, [e.target.name]: e.target.value });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (customer.name && customer.email && customer.phone) {
      setCustomers([...customers, customer]);
      setCustomer({ name: '', email: '', phone: '' });
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <input type="text" name="name" placeholder="Name" value={customer.name} onChange={handleChange} required />
        <input type="email" name="email" placeholder="Email" value={customer.email} onChange={handleChange} required />
        <input type="tel" name="phone" placeholder="Phone" value={customer.phone} onChange={handleChange} required />
        <button type="submit">Add Customer</button>
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