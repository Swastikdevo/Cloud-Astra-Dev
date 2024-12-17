```javascript
import React, { useState } from 'react';

const Customers = () => {
  const [customers, setCustomers] = useState([]);
  const [newCustomer, setNewCustomer] = useState('');
  const [editIndex, setEditIndex] = useState(null);
  const [editValue, setEditValue] = useState('');

  const addCustomer = () => {
    if (newCustomer) {
      setCustomers([...customers, newCustomer]);
      setNewCustomer('');
    }
  };

  const editCustomer = (index) => {
    setEditIndex(index);
    setEditValue(customers[index]);
  };

  const updateCustomer = () => {
    const updatedCustomers = [...customers];
    updatedCustomers[editIndex] = editValue;
    setCustomers(updatedCustomers);
    setEditIndex(null);
    setEditValue('');
  };

  const deleteCustomer = (index) => {
    const updatedCustomers = customers.filter((_, i) => i !== index);
    setCustomers(updatedCustomers);
  };

  return (
    <div>
      <h2>Customer Management</h2>
      <input 
        type="text" 
        value={newCustomer} 
        onChange={(e) => setNewCustomer(e.target.value)} 
        placeholder="Add new customer" 
      />
      <button onClick={addCustomer}>Add</button>
      <ul>
        {customers.map((customer, index) => (
          <li key={index}>
            {editIndex === index ? (
              <>
                <input 
                  type="text" 
                  value={editValue} 
                  onChange={(e) => setEditValue(e.target.value)} 
                />
                <button onClick={updateCustomer}>Save</button>
              </>
            ) : (
              <>
                {customer}
                <button onClick={() => editCustomer(index)}>Edit</button>
                <button onClick={() => deleteCustomer(index)}>Delete</button>
              </>
            )}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default Customers;
```