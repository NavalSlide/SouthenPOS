def business_settings(request):
    """
    Context processor to add business settings to all templates
    """
    context = {}
    if request.user.is_authenticated:
        try:
            business = request.user.business
            context['currency_symbol'] = business.moneda
            
            # Add theme settings
            context['theme_settings'] = {
                'primary_color': business.primary_color,
                'primary_color_rgb': business.primary_color.lstrip('#'),
                'secondary_color': business.secondary_color,
                'secondary_color_rgb': business.secondary_color.lstrip('#'),
            }
            
            # Add dark mode setting
            context['dark_mode'] = business.dark_mode
            
            # Add custom brand name if enabled
            if business.use_custom_brand_name and business.custom_brand_name:
                context['brand_name'] = business.custom_brand_name
            else:
                context['brand_name'] = 'SouthernPOS'
                
        except:
            # Default values if business doesn't exist
            context['currency_symbol'] = '$'
            context['theme_settings'] = {
                'primary_color': '#10b981',
                'primary_color_rgb': '16, 185, 129',
                'secondary_color': '#6366f1',
                'secondary_color_rgb': '99, 102, 241',
            }
            context['dark_mode'] = False
            context['brand_name'] = 'SouthernPOS'
    
    return context