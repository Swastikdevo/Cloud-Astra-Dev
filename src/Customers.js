```javascript
import React, { useState, useEffect } from 'react';

const CustomerManagement = () => {
    const [customers, setCustomers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState('');

    useEffect(() => {
        fetchCustomers();
    }, []);

    const fetchCustomers = async () => {
        setLoading(true);
        const response = await fetch('/api/customers');
        const data = await response.json();
        setCustomers(data);
        setLoading(false);
    };

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(searchTerm.toLowerCase())
    );

    const handleSearchChange = (e) => {
        setSearchTerm(e.target.value);
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search Customers..." 
                value={searchTerm} 
                onChange={handleSearchChange} 
            />
            {loading ? (
                <p>Loading...</p>
            ) : (
                <ul>
                    {filteredCustomers.map(customer => (
                        <li key={customer.id}>{customer.name} - {customer.email}</li>
                    ))}
                </ul>
            )}
        </div>
    );
};

export default CustomerManagement;
```