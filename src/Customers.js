```javascript
import React, { useState, useEffect } from 'react';

const CustomerForm = ({ onSubmit, customer }) => {
  const [name, setName] = useState(customer ? customer.name : '');
  const [email, setEmail] = useState(customer ? customer.email : '');
  const [phone, setPhone] = useState(customer ? customer.phone : '');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit({ name, email, phone });
  };

  return (
    <form onSubmit={handleSubmit}>
      <input type="text" placeholder="Name" value={name} onChange={(e) => setName(e.target.value)} required />
      <input type="email" placeholder="Email" value={email} onChange={(e) => setEmail(e.target.value)} required />
      <input type="tel" placeholder="Phone" value={phone} onChange={(e) => setPhone(e.target.value)} required />
      <button type="submit">Submit</button>
    </form>
  );
};

const CustomerList = ({ customers, onEdit, onDelete }) => {
  return (
    <ul>
      {customers.map((customer) => (
        <li key={customer.id}>
          {customer.name} - {customer.email} - {customer.phone}
          <button onClick={() => onEdit(customer)}>Edit</button>
          <button onClick={() => onDelete(customer.id)}>Delete</button>
        </li>
      ))}
    </ul>
  );
};

const CustomerManagement = () => {
  const [customers, setCustomers] = useState([]);
  const [editingCustomer, setEditingCustomer] = useState(null);

  useEffect(() => {
    const fetchCustomers = async () => {
      const response = await fetch('/api/customers');
      const data = await response.json();
      setCustomers(data);
    };
    fetchCustomers();
  }, []);

  const handleAddOrUpdate = async (customerData) => {
    if (editingCustomer) {
      await fetch(`/api/customers/${editingCustomer.id}`, {
        method: 'PUT',
        body: JSON.stringify(customerData),
        headers: { 'Content-Type': 'application/json' },
      });
      setEditingCustomer(null);
    } else {
      await fetch('/api/customers', {
        method: 'POST',
        body: JSON.stringify(customerData),
        headers: { 'Content-Type': 'application/json' },
      });
    }
    setCustomers(await (await fetch('/api/customers')).json());
  };

  const handleEdit = (customer) => {
    setEditingCustomer(customer);
  };

  const handleDelete = async (id) => {
    await fetch(`/api/customers/${id}`, { method: 'DELETE' });
    setCustomers(await (await fetch('/api/customers')).json());
  };

  return (
    <div>
      <h1>Customer Management</h1>
      <CustomerForm onSubmit={handleAddOrUpdate} customer={editingCustomer} />
      <CustomerList customers={customers} onEdit={handleEdit} onDelete={handleDelete} />
    </div>
  );
};

export default CustomerManagement;
```