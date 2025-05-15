```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit, customer = {} }) => {
  const [name, setName] = useState(customer.name || '');
  const [email, setEmail] = useState(customer.email || '');
  const [phone, setPhone] = useState(customer.phone || '');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, email, phone });
  };

  useEffect(() => {
    if (customer) {
      setName(customer.name);
      setEmail(customer.email);
      setPhone(customer.phone);
    }
  }, [customer]);

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" value={name} onChange={(e) => setName(e.target.value)} placeholder="Name" required />
      <input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="Email" required />
      <input type="tel" value={phone} onChange={(e) => setPhone(e.target.value)} placeholder="Phone" required />
      <button type="submit">Save Customer</button>
    </form>
  );
};

const CustomerList = ({ customers, onDelete }) => {
  return (
    <ul>
      {customers.map((customer, index) => (
        <li key={index}>
          {customer.name} ({customer.email}) - {customer.phone}
          <button onClick={() => onDelete(index)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

const CustomerManager = () => {
  const [customers, setCustomers] = useState([]);
  const [editingCustomer, setEditingCustomer] = useState(null);

  const handleAddOrUpdateCustomer = (customer) => {
    if (editingCustomer !== null) {
      const updatedCustomers = [...customers];
      updatedCustomers[editingCustomer] = customer;
      setCustomers(updatedCustomers);
      setEditingCustomer(null);
    } else {
      setCustomers([...customers, customer]);
    }
  };

  const handleDeleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
  };

  const handleEditCustomer = (index) => {
    setEditingCustomer(index);
  };

  return (
    <div>
      <CustomerForm onSubmit={handleAddOrUpdateCustomer} customer={editingCustomer !== null ? customers[editingCustomer] : {}} />
      <CustomerList customers={customers} onDelete={handleDeleteCustomer} />
    </div>
  );
};

export default CustomerManager;
```