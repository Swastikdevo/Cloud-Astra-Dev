```javascript
import React, { useState, useEffect } from 'react';

const CustomerList = () => {
    const [customers, setCustomers] = useState([]);
    const [filter, setFilter] = useState('');
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchCustomers = async () => {
            const response = await fetch('/api/customers');
            const data = await response.json();
            setCustomers(data);
            setLoading(false);
        };
        fetchCustomers();
    }, []);

    const filteredCustomers = customers.filter(customer => 
        customer.name.toLowerCase().includes(filter.toLowerCase())
    );

    const handleInputChange = (e) => {
        setFilter(e.target.value);
    };

    return (
        <div>
            <input 
                type="text" 
                placeholder="Search Customers" 
                value={filter} 
                onChange={handleInputChange} 
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

export default CustomerList;
```