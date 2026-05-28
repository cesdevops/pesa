# Create your views here.
from decimal import Decimal
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.shortcuts import render, redirect

from FundRelease.models import Kosh_Fund_Allocation
from Main.models import Kosh_Head
from Main.utils import validate_clean_text
from Kosh.models import Kosh, Kosh_User

from Activity.models import Activity, Work_Master,Administrative_Sanction
from decimal import Decimal
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from datetime import datetime
from .models import Technical_Sanction, Work_Master, Work_Order, Work_Start
from Kosh.utils import switch_kosh

def Activity_Work_Master(request):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(
            id=user_id,
            status='Active'
        )

    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # User Accessible Kosh IDs
    user_kosh_ids = kosh_user.kosh.values_list('id', flat=True)

    # Work Master List
    work_masters = Work_Master.objects.filter(
        kosh_fund_allocation__kosh_id__in=user_kosh_ids
    ).select_related(
        'activity',
        'kosh_fund_allocation',
        'kosh_fund_allocation__kosh'
    ).order_by('-id')

    # Filters
    work_name = request.GET.get('work_name', '').strip()
    work_code = request.GET.get('work_code', '').strip()
    overall_status = request.GET.get('overall_status', '').strip()

    if work_name:
        work_masters = work_masters.filter(
            work_name__icontains=work_name
        )

    if work_code:
        work_masters = work_masters.filter(
            work_code__icontains=work_code
        )

    if overall_status:
        work_masters = work_masters.filter(
            overall_status=overall_status
        )

    # Pagination
    paginator = Paginator(work_masters, 15)

    page_number = request.GET.get('page')
    work_masters = paginator.get_page(page_number)

    context = {
        'user_type': 'Kosh',
        
        'kosh_user': kosh_user,
        'work_masters': work_masters,
        'work_name': work_name,
        'work_code': work_code,
        'overall_status': overall_status,
        'status_choices': Work_Master.WORK_STATUS_CHOICES,
    }

    return render(
        request,
        'Activity-Work-Master.html',
        context
    )

def Activity_Add_Work_Master(request):

    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(
            id=user_id,
            status='Active'
        )

    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # User Kosh IDs
    user_kosh_ids = kosh_user.kosh.values_list('id', flat=True)

    # Kosh Heads
    kosh_heads = Kosh_Head.objects.filter(
        status='Active'
    ).order_by('name')

    # Activities
    activities = Activity.objects.filter(
        status='Active'
    ).select_related('kosh_head').order_by('kosh_head__name', 'activity_name')

    # Kosh Fund Allocation
    active_kosh_id = request.session.get('active_kosh_id')

    active_kosh = Kosh.objects.filter(
        id=active_kosh_id,
        status='Active',
        is_deleted=False
    ).first()

    # Active Kosh Allocation
    kosh_fund_allocation = Kosh_Fund_Allocation.objects.filter(
        kosh_id=active_kosh_id
    ).select_related('kosh').first()

    if request.method == "POST":

        activity_id = request.POST.get('activity')

        work_name = request.POST.get('work_name')
        work_code = request.POST.get('work_code')
        work_description = request.POST.get('work_description')
        work_location = request.POST.get('work_location')

        estimated_amount = request.POST.get(
            'estimated_amount'
        )

        approved_amount = request.POST.get(
            'approved_amount'
        )

        overall_status = request.POST.get(
            'overall_status'
        )

        Work_Master.objects.create(
            activity_id=activity_id,
            kosh_fund_allocation=kosh_fund_allocation,
            work_name=work_name,
            work_code=work_code,
            work_description=work_description,
            work_location=work_location,
            estimated_amount=estimated_amount or 0,
            approved_amount=approved_amount or 0,
            overall_status=overall_status,

            created_by=kosh_user,
            updated_by=kosh_user,
        )

        messages.success(
            request,
            "Work Master Added Successfully"
        )

        return redirect('Activity-Work-Master')

    context = {

        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'kosh_heads': kosh_heads,
        'activities': activities,
        'active_kosh': active_kosh,
        'status_choices': Work_Master.WORK_STATUS_CHOICES,
        # 'load_sidebar': "load_sidebar",
    }

    return render(
        request,
        'Activity-Add-Work-Master.html',
        context
    )


def Activity_Administrative_Sanction(request, work_id):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # Get Work Master by ID
    work_master = get_object_or_404(Work_Master, id=work_id)
    
    # Check if Administrative Sanction already exists
    try:
        admin_sanction = Administrative_Sanction.objects.get(work_master=work_master)
        is_edit = True
    except Administrative_Sanction.DoesNotExist:
        admin_sanction = None
        is_edit = False

    if request.method == 'POST':
        try:
            # Get form data with proper handling for empty values
            sanction_number = request.POST.get('sanction_number', '').strip() or None
            department_name = request.POST.get('department_name', '').strip() or None
            
            # Handle estimated amount - update both admin sanction and work master
            estimated_amount_str = request.POST.get('estimated_amount', '')
            estimated_amount = None
            if estimated_amount_str and estimated_amount_str.strip():
                try:
                    estimated_amount = Decimal(str(estimated_amount_str))
                except:
                    estimated_amount = None
            
            # Handle approved amount - update both admin sanction and work master
            approved_amount_str = request.POST.get('approved_amount', '')
            approved_amount = None
            if approved_amount_str and approved_amount_str.strip():
                try:
                    approved_amount = Decimal(str(approved_amount_str))
                except:
                    approved_amount = None
            
            # Handle dates - convert empty strings to None
            sanction_date = None
            sanction_date_str = request.POST.get('sanction_date', '')
            if sanction_date_str and sanction_date_str.strip():
                try:
                    sanction_date = sanction_date_str
                except Exception as e:
                    messages.warning(request, f"मान्यता दिनांक फॉरमॅट अयोग्य: {e}")
            
            proposal_date = None
            proposal_date_str = request.POST.get('proposal_date', '')
            if proposal_date_str and proposal_date_str.strip():
                try:
                    proposal_date = proposal_date_str
                except Exception as e:
                    messages.warning(request, f"प्रस्ताव दिनांक फॉरमॅट अयोग्य: {e}")
            
            resolution_date = None
            resolution_date_str = request.POST.get('resolution_date', '')
            if resolution_date_str and resolution_date_str.strip():
                try:
                    resolution_date = resolution_date_str
                except Exception as e:
                    messages.warning(request, f"ठराव दिनांक फॉरमॅट अयोग्य: {e}")
            
            work_location = request.POST.get('work_location', '').strip() or None
            objective = request.POST.get('objective', '').strip() or None
            beneficiary_details = request.POST.get('beneficiary_details', '').strip() or None
            resolution_number = request.POST.get('resolution_number', '').strip() or None
            remarks = request.POST.get('remarks', '').strip() or None
            status = request.POST.get('status', 'Pending')
            
            # Handle file uploads
            resolution_document = request.FILES.get('resolution_document')
            proposal_document = request.FILES.get('proposal_document')
            budget_estimate_document = request.FILES.get('budget_estimate_document')
            approval_letter_document = request.FILES.get('approval_letter_document')
            other_document = request.FILES.get('other_document')
            
            if is_edit:
                # Update existing record
                admin_sanction.sanction_number = sanction_number
                admin_sanction.department_name = department_name
                admin_sanction.estimated_amount = estimated_amount
                admin_sanction.approved_amount = approved_amount
                admin_sanction.sanction_date = sanction_date
                admin_sanction.proposal_date = proposal_date
                admin_sanction.work_location = work_location
                admin_sanction.objective = objective
                admin_sanction.beneficiary_details = beneficiary_details
                admin_sanction.resolution_number = resolution_number
                admin_sanction.resolution_date = resolution_date
                admin_sanction.remarks = remarks
                admin_sanction.status = status
                admin_sanction.updated_at = timezone.now()
                
                # Update documents only if new files are uploaded
                if resolution_document:
                    admin_sanction.resolution_document = resolution_document
                if proposal_document:
                    admin_sanction.proposal_document = proposal_document
                if budget_estimate_document:
                    admin_sanction.budget_estimate_document = budget_estimate_document
                if approval_letter_document:
                    admin_sanction.approval_letter_document = approval_letter_document
                if other_document:
                    admin_sanction.other_document = other_document
                    
                admin_sanction.save()
                
                # Update Work Master amounts if they are provided
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if approved_amount is not None:
                    work_master.approved_amount = approved_amount
                work_master.save()
                
                messages.success(request, "प्रशासकीय मान्यता यशस्वीरित्या अद्यतनित केली")
            else:
                # Create new record
                admin_sanction = Administrative_Sanction.objects.create(
                    work_master=work_master,
                    sanction_number=sanction_number,
                    department_name=department_name,
                    estimated_amount=estimated_amount,
                    approved_amount=approved_amount,
                    sanction_date=sanction_date,
                    proposal_date=proposal_date,
                    work_location=work_location,
                    objective=objective,
                    beneficiary_details=beneficiary_details,
                    resolution_number=resolution_number,
                    resolution_date=resolution_date,
                    remarks=remarks,
                    status=status,
                    resolution_document=resolution_document,
                    proposal_document=proposal_document,
                    budget_estimate_document=budget_estimate_document,
                    approval_letter_document=approval_letter_document,
                    other_document=other_document,
                    created_by=kosh_user
                )
                
                # Update Work Master amounts if they are provided
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if approved_amount is not None:
                    work_master.approved_amount = approved_amount
                work_master.save()
                
                messages.success(request, "प्रशासकीय मान्यता यशस्वीरित्या जतन केली")
            
            # Update Work Master status if administrative sanction is completed
            if status == 'Approved':
                work_master.administrative_sanction_completed = True
                work_master.administrative_sanction_completed_date = timezone.now()
                work_master.administrative_sanction_status = 'Approved'
                work_master.overall_status = 'In Progress'
                work_master.save()
            elif status == 'Rejected':
                work_master.administrative_sanction_status = 'Rejected'
                work_master.administrative_sanction_completed = False
                work_master.save()
            
            return redirect('Activity-Administrative-Sanction', work_id=work_id)
            
        except Exception as e:
            # Handle any unexpected errors
            messages.error(request, f"एरर आली: {str(e)}")
            context = {
                'user_type': 'Kosh',
                'kosh_user': kosh_user,
                'work_master': work_master,
                'admin_sanction': admin_sanction,
                'is_edit': is_edit,
                'load_sidebar': "load_sidebar",
            }
            return render(request, 'Activity-Administrative-Sanction.html', context)

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'work_master': work_master,
        'admin_sanction': admin_sanction,
        'is_edit': is_edit,
        'load_sidebar': "load_sidebar",
        **switch_kosh(request),
    }

    return render(request, 'Activity-Administrative-Sanction.html', context)


def Activity_Technical_Sanction(request, work_id):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # Get Work Master by ID
    work_master = get_object_or_404(Work_Master, id=work_id)
    
    # Check if Technical Sanction already exists
    try:
        tech_sanction = Technical_Sanction.objects.get(work_master=work_master)
        is_edit = True
    except Technical_Sanction.DoesNotExist:
        tech_sanction = None
        is_edit = False

    if request.method == 'POST':
        try:
            # Get form data with proper handling for empty values
            technical_sanction_number = request.POST.get('technical_sanction_number', '').strip() or None
            technical_category = request.POST.get('technical_category', '').strip() or None
            
            # Handle estimated amount - update both tech sanction and work master
            estimated_amount_str = request.POST.get('estimated_amount', '')
            estimated_amount = None
            if estimated_amount_str and estimated_amount_str.strip():
                try:
                    estimated_amount = Decimal(str(estimated_amount_str))
                except:
                    estimated_amount = None
            
            # Handle approved amount - update both tech sanction and work master
            approved_amount_str = request.POST.get('approved_amount', '')
            approved_amount = None
            if approved_amount_str and approved_amount_str.strip():
                try:
                    approved_amount = Decimal(str(approved_amount_str))
                except:
                    approved_amount = None
            
            # Handle dates - convert empty strings to None
            sanction_date = None
            sanction_date_str = request.POST.get('sanction_date', '')
            if sanction_date_str and sanction_date_str.strip():
                try:
                    sanction_date = sanction_date_str
                except Exception as e:
                    messages.warning(request, f"मान्यता दिनांक फॉरमॅट अयोग्य: {e}")
            
            inspection_date = None
            inspection_date_str = request.POST.get('inspection_date', '')
            if inspection_date_str and inspection_date_str.strip():
                try:
                    inspection_date = inspection_date_str
                except Exception as e:
                    messages.warning(request, f"तपासणी दिनांक फॉरमॅट अयोग्य: {e}")
            
            # Get text fields
            technical_specification = request.POST.get('technical_specification', '').strip() or None
            work_scope = request.POST.get('work_scope', '').strip() or None
            site_details = request.POST.get('site_details', '').strip() or None
            measurement_details = request.POST.get('measurement_details', '').strip() or None
            material_details = request.POST.get('material_details', '').strip() or None
            engineer_name = request.POST.get('engineer_name', '').strip() or None
            engineer_designation = request.POST.get('engineer_designation', '').strip() or None
            approval_remark = request.POST.get('approval_remark', '').strip() or None
            status = request.POST.get('status', 'Pending')
            
            # Handle file uploads
            technical_estimate_document = request.FILES.get('technical_estimate_document')
            site_inspection_document = request.FILES.get('site_inspection_document')
            engineer_report_document = request.FILES.get('engineer_report_document')
            drawing_plan_document = request.FILES.get('drawing_plan_document')
            approval_letter_document = request.FILES.get('approval_letter_document')
            other_document = request.FILES.get('other_document')
            
            if is_edit:
                # Update existing record
                tech_sanction.technical_sanction_number = technical_sanction_number
                tech_sanction.technical_category = technical_category
                tech_sanction.estimated_amount = estimated_amount
                tech_sanction.approved_amount = approved_amount
                tech_sanction.sanction_date = sanction_date
                tech_sanction.inspection_date = inspection_date
                tech_sanction.technical_specification = technical_specification
                tech_sanction.work_scope = work_scope
                tech_sanction.site_details = site_details
                tech_sanction.measurement_details = measurement_details
                tech_sanction.material_details = material_details
                tech_sanction.engineer_name = engineer_name
                tech_sanction.engineer_designation = engineer_designation
                tech_sanction.approval_remark = approval_remark
                tech_sanction.status = status
                tech_sanction.updated_at = timezone.now()
                
                # Update documents only if new files are uploaded
                if technical_estimate_document:
                    tech_sanction.technical_estimate_document = technical_estimate_document
                if site_inspection_document:
                    tech_sanction.site_inspection_document = site_inspection_document
                if engineer_report_document:
                    tech_sanction.engineer_report_document = engineer_report_document
                if drawing_plan_document:
                    tech_sanction.drawing_plan_document = drawing_plan_document
                if approval_letter_document:
                    tech_sanction.approval_letter_document = approval_letter_document
                if other_document:
                    tech_sanction.other_document = other_document
                    
                tech_sanction.save()
                
                # Update Work Master amounts if they are provided
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if approved_amount is not None:
                    work_master.approved_amount = approved_amount
                work_master.save()
                
                messages.success(request, "तांत्रिक मान्यता यशस्वीरित्या अद्यतनित केली")
            else:
                # Create new record
                tech_sanction = Technical_Sanction.objects.create(
                    work_master=work_master,
                    technical_sanction_number=technical_sanction_number,
                    technical_category=technical_category,
                    estimated_amount=estimated_amount,
                    approved_amount=approved_amount,
                    sanction_date=sanction_date,
                    inspection_date=inspection_date,
                    technical_specification=technical_specification,
                    work_scope=work_scope,
                    site_details=site_details,
                    measurement_details=measurement_details,
                    material_details=material_details,
                    engineer_name=engineer_name,
                    engineer_designation=engineer_designation,
                    approval_remark=approval_remark,
                    status=status,
                    technical_estimate_document=technical_estimate_document,
                    site_inspection_document=site_inspection_document,
                    engineer_report_document=engineer_report_document,
                    drawing_plan_document=drawing_plan_document,
                    approval_letter_document=approval_letter_document,
                    other_document=other_document,
                    created_by=kosh_user
                )
                
                # Update Work Master amounts if they are provided
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if approved_amount is not None:
                    work_master.approved_amount = approved_amount
                work_master.save()
                
                messages.success(request, "तांत्रिक मान्यता यशस्वीरित्या जतन केली")
            
            # Update Work Master status if technical sanction is completed
            if status == 'Approved':
                work_master.technical_sanction_completed = True
                work_master.technical_sanction_completed_date = timezone.now()
                work_master.technical_sanction_status = 'Approved'
                work_master.save()
            elif status == 'Rejected':
                work_master.technical_sanction_status = 'Rejected'
                work_master.technical_sanction_completed = False
                work_master.save()
            
            return redirect('Activity-Technical-Sanction', work_id=work_id)
            
        except Exception as e:
            # Handle any unexpected errors
            messages.error(request, f"एरर आली: {str(e)}")
            context = {
                'user_type': 'Kosh',
                'kosh_user': kosh_user,
                'work_master': work_master,
                'tech_sanction': tech_sanction,
                'is_edit': is_edit,
                'load_sidebar': "load_sidebar",
            }
            return render(request, 'Activity-Technical-Sanction.html', context)

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'work_master': work_master,
        'tech_sanction': tech_sanction,
        'is_edit': is_edit,
        'load_sidebar': "load_sidebar",
    }

    return render(request, 'Activity-Technical-Sanction.html', context)


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Work_Master, Administrative_Sanction, Technical_Sanction, Quotation_Tender, Kosh_User

def Activity_Quotation_Tender(request, work_id):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # Get Work Master by ID
    work_master = get_object_or_404(Work_Master, id=work_id)
    
    # Check if Quotation/Tender already exists
    try:
        quotation_tender = Quotation_Tender.objects.get(work_master=work_master)
        is_edit = True
    except Quotation_Tender.DoesNotExist:
        quotation_tender = None
        is_edit = False

    if request.method == 'POST':
        try:
            # Get form data with proper handling for empty values
            process_type = request.POST.get('process_type', '').strip() or None
            process_number = request.POST.get('process_number', '').strip() or None
            work_name = request.POST.get('work_name', '').strip() or None
            work_description = request.POST.get('work_description', '').strip() or None
            vendor_name = request.POST.get('vendor_name', '').strip() or None
            contractor_name = request.POST.get('contractor_name', '').strip() or None
            contractor_mobile = request.POST.get('contractor_mobile', '').strip() or None
            contractor_address = request.POST.get('contractor_address', '').strip() or None
            comparative_analysis = request.POST.get('comparative_analysis', '').strip() or None
            selection_reason = request.POST.get('selection_reason', '').strip() or None
            remarks = request.POST.get('remarks', '').strip() or None
            status = request.POST.get('status', 'Pending')
            
            # Handle amounts
            estimated_amount_str = request.POST.get('estimated_amount', '')
            estimated_amount = None
            if estimated_amount_str and estimated_amount_str.strip():
                try:
                    estimated_amount = Decimal(str(estimated_amount_str))
                except:
                    estimated_amount = None
            
            finalized_amount_str = request.POST.get('finalized_amount', '')
            finalized_amount = None
            if finalized_amount_str and finalized_amount_str.strip():
                try:
                    finalized_amount = Decimal(str(finalized_amount_str))
                except:
                    finalized_amount = None
            
            # Handle dates
            process_date = None
            process_date_str = request.POST.get('process_date', '')
            if process_date_str and process_date_str.strip():
                try:
                    process_date = process_date_str
                except Exception as e:
                    messages.warning(request, f"प्रक्रिया दिनांक फॉरमॅट अयोग्य: {e}")
            
            # Handle file uploads
            quotation_form_document = request.FILES.get('quotation_form_document')
            comparative_statement_document = request.FILES.get('comparative_statement_document')
            contractor_agreement_document = request.FILES.get('contractor_agreement_document')
            tender_document = request.FILES.get('tender_document')
            other_document = request.FILES.get('other_document')
            
            if is_edit:
                # Update existing record
                quotation_tender.process_type = process_type
                quotation_tender.process_number = process_number
                quotation_tender.process_date = process_date
                quotation_tender.work_name = work_name
                quotation_tender.work_description = work_description
                quotation_tender.estimated_amount = estimated_amount
                quotation_tender.finalized_amount = finalized_amount
                quotation_tender.vendor_name = vendor_name
                quotation_tender.contractor_name = contractor_name
                quotation_tender.contractor_mobile = contractor_mobile
                quotation_tender.contractor_address = contractor_address
                quotation_tender.comparative_analysis = comparative_analysis
                quotation_tender.selection_reason = selection_reason
                quotation_tender.remarks = remarks
                quotation_tender.status = status
                quotation_tender.updated_at = timezone.now()
                
                # Update documents only if new files are uploaded
                if quotation_form_document:
                    quotation_tender.quotation_form_document = quotation_form_document
                if comparative_statement_document:
                    quotation_tender.comparative_statement_document = comparative_statement_document
                if contractor_agreement_document:
                    quotation_tender.contractor_agreement_document = contractor_agreement_document
                if tender_document:
                    quotation_tender.tender_document = tender_document
                if other_document:
                    quotation_tender.other_document = other_document
                    
                quotation_tender.save()
                
                # Update Work Master amounts if provided
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if finalized_amount is not None:
                    work_master.approved_amount = finalized_amount
                work_master.save()
                
                messages.success(request, "कोटेशन/बी1/निविदा यशस्वीरित्या अद्यतनित केली")
            else:
                # Create new record
                quotation_tender = Quotation_Tender.objects.create(
                    work_master=work_master,
                    process_type=process_type,
                    process_number=process_number,
                    process_date=process_date,
                    work_name=work_name,
                    work_description=work_description,
                    estimated_amount=estimated_amount,
                    finalized_amount=finalized_amount,
                    vendor_name=vendor_name,
                    contractor_name=contractor_name,
                    contractor_mobile=contractor_mobile,
                    contractor_address=contractor_address,
                    comparative_analysis=comparative_analysis,
                    selection_reason=selection_reason,
                    remarks=remarks,
                    status=status,
                    quotation_form_document=quotation_form_document,
                    comparative_statement_document=comparative_statement_document,
                    contractor_agreement_document=contractor_agreement_document,
                    tender_document=tender_document,
                    other_document=other_document,
                    created_by=kosh_user
                )
                
                # Update Work Master amounts if provided
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if finalized_amount is not None:
                    work_master.approved_amount = finalized_amount
                work_master.save()
                
                messages.success(request, "कोटेशन/बी1/निविदा यशस्वीरित्या जतन केली")
            
            # Update Work Master status based on process status
            if status == 'Contractor Finalized' or status == 'Approved':
                work_master.quotation_tender_completed = True
                work_master.quotation_tender_completed_date = timezone.now()
                work_master.quotation_tender_status = 'Completed'
                work_master.contractor_name = contractor_name or quotation_tender.contractor_name
                work_master.contractor_finalized = True
                work_master.contractor_finalized_date = timezone.now()
                work_master.save()
            elif status == 'Rejected':
                work_master.quotation_tender_status = 'Rejected'
                work_master.quotation_tender_completed = False
                work_master.save()
            
            return redirect('Activity-Quotation-Tender', work_id=work_id)
            
        except Exception as e:
            # Handle any unexpected errors
            messages.error(request, f"एरर आली: {str(e)}")
            context = {
                'user_type': 'Kosh',
                'kosh_user': kosh_user,
                'work_master': work_master,
                'quotation_tender': quotation_tender,
                'is_edit': is_edit,
                'load_sidebar': "load_sidebar",
            }
            return render(request, 'Activity-Quotation-Tender.html', context)

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'work_master': work_master,
        'quotation_tender': quotation_tender,
        'is_edit': is_edit,
        'load_sidebar': "load_sidebar",
    }

    return render(request, 'Activity-Quotation-Tender.html', context)

def Activity_Work_Order(request, work_id):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # Get Work Master by ID
    work_master = get_object_or_404(Work_Master, id=work_id)
    
    # Check if Work Order already exists
    try:
        work_order = Work_Order.objects.get(work_master=work_master)
        is_edit = True
    except Work_Order.DoesNotExist:
        work_order = None
        is_edit = False

    if request.method == 'POST':
        try:
            # Get form data
            work_order_number = request.POST.get('work_order_number', '').strip() or None
            work_name = request.POST.get('work_name', '').strip() or None
            work_description = request.POST.get('work_description', '').strip() or None
            contractor_name = request.POST.get('contractor_name', '').strip() or None
            contractor_mobile = request.POST.get('contractor_mobile', '').strip() or None
            contractor_address = request.POST.get('contractor_address', '').strip() or None
            category = request.POST.get('category', '').strip() or None
            execution_instructions = request.POST.get('execution_instructions', '').strip() or None
            remarks = request.POST.get('remarks', '').strip() or None
            status = request.POST.get('status', 'Pending')
            
            # Handle amounts
            estimated_amount_str = request.POST.get('estimated_amount', '')
            estimated_amount = None
            if estimated_amount_str and estimated_amount_str.strip():
                try:
                    estimated_amount = Decimal(str(estimated_amount_str))
                except:
                    estimated_amount = None
            
            approved_amount_str = request.POST.get('approved_amount', '')
            approved_amount = None
            if approved_amount_str and approved_amount_str.strip():
                try:
                    approved_amount = Decimal(str(approved_amount_str))
                except:
                    approved_amount = None
            
            # Handle dates
            work_order_date = None
            work_order_date_str = request.POST.get('work_order_date', '')
            if work_order_date_str and work_order_date_str.strip():
                try:
                    work_order_date = work_order_date_str
                except:
                    pass
            
            work_start_date = None
            work_start_date_str = request.POST.get('work_start_date', '')
            if work_start_date_str and work_start_date_str.strip():
                try:
                    work_start_date = work_start_date_str
                except:
                    pass
            
            expected_completion_date = None
            expected_completion_date_str = request.POST.get('expected_completion_date', '')
            if expected_completion_date_str and expected_completion_date_str.strip():
                try:
                    expected_completion_date = expected_completion_date_str
                except:
                    pass
            
            actual_completion_date = None
            actual_completion_date_str = request.POST.get('actual_completion_date', '')
            if actual_completion_date_str and actual_completion_date_str.strip():
                try:
                    actual_completion_date = actual_completion_date_str
                except:
                    pass
            
            # Handle file uploads
            signed_work_order_document = request.FILES.get('signed_work_order_document')
            agreement_document = request.FILES.get('agreement_document')
            other_document = request.FILES.get('other_document')
            
            if is_edit:
                # Update existing record
                work_order.work_order_number = work_order_number
                work_order.work_name = work_name
                work_order.work_description = work_description
                work_order.contractor_name = contractor_name
                work_order.contractor_mobile = contractor_mobile
                work_order.contractor_address = contractor_address
                work_order.work_order_date = work_order_date
                work_order.work_start_date = work_start_date
                work_order.expected_completion_date = expected_completion_date
                work_order.actual_completion_date = actual_completion_date
                work_order.estimated_amount = estimated_amount
                work_order.approved_amount = approved_amount
                work_order.category = category
                work_order.execution_instructions = execution_instructions
                work_order.remarks = remarks
                work_order.status = status
                work_order.updated_at = timezone.now()
                work_order.updated_by = kosh_user
                
                # Update documents
                if signed_work_order_document:
                    work_order.signed_work_order_document = signed_work_order_document
                if agreement_document:
                    work_order.agreement_document = agreement_document
                if other_document:
                    work_order.other_document = other_document
                    
                work_order.save()
                
                # Update Work Master
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if approved_amount is not None:
                    work_master.approved_amount = approved_amount
                if contractor_name:
                    work_master.contractor_name = contractor_name
                work_master.save()
                
                messages.success(request, "वर्क ऑर्डर यशस्वीरित्या अद्यतनित केली")
            else:
                # Create new record
                work_order = Work_Order.objects.create(
                    work_master=work_master,
                    work_order_number=work_order_number,
                    work_name=work_name,
                    work_description=work_description,
                    contractor_name=contractor_name,
                    contractor_mobile=contractor_mobile,
                    contractor_address=contractor_address,
                    work_order_date=work_order_date,
                    work_start_date=work_start_date,
                    expected_completion_date=expected_completion_date,
                    actual_completion_date=actual_completion_date,
                    estimated_amount=estimated_amount,
                    approved_amount=approved_amount,
                    category=category,
                    execution_instructions=execution_instructions,
                    remarks=remarks,
                    status=status,
                    signed_work_order_document=signed_work_order_document,
                    agreement_document=agreement_document,
                    other_document=other_document,
                    created_by=kosh_user
                )
                
                # Update Work Master
                if estimated_amount is not None:
                    work_master.estimated_amount = estimated_amount
                if approved_amount is not None:
                    work_master.approved_amount = approved_amount
                if contractor_name:
                    work_master.contractor_name = contractor_name
                work_master.save()
                
                messages.success(request, "वर्क ऑर्डर यशस्वीरित्या जतन केली")
            
            # Update Work Master status
            if status == 'Completed':
                work_master.work_order_completed = True
                work_master.work_order_completed_date = timezone.now()
                work_master.work_order_status = 'Completed'
                work_master.save()
            
            return redirect('Activity-Work-Order', work_id=work_id)
            
        except Exception as e:
            messages.error(request, f"एरर आली: {str(e)}")

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'work_master': work_master,
        'work_order': work_order,
        'is_edit': is_edit,
        'load_sidebar': "load_sidebar",
    }

    return render(request, 'Activity-Work-Order.html', context)


def Activity_Work_Start(request, work_id):
    if request.session.get('user_type') != 'Kosh':
        messages.error(request, "Unauthorized Access")
        return redirect('Login')

    user_id = request.session.get('user_id')

    try:
        kosh_user = Kosh_User.objects.get(id=user_id, status='Active')
    except Kosh_User.DoesNotExist:
        messages.error(request, "User Not Found")
        return redirect('Login')

    # Get Work Master by ID
    work_master = get_object_or_404(Work_Master, id=work_id)
    
    # Check if Work Start already exists
    try:
        work_start = Work_Start.objects.get(work_master=work_master)
        is_edit = True
    except Work_Start.DoesNotExist:
        work_start = None
        is_edit = False

    if request.method == 'POST':
        try:
            # Get form data
            site_location = request.POST.get('site_location', '').strip() or None
            supervisor_name = request.POST.get('supervisor_name', '').strip() or None
            contractor_name = request.POST.get('contractor_name', '').strip() or None
            initial_work_status = request.POST.get('initial_work_status', '').strip() or None
            remarks = request.POST.get('remarks', '').strip() or None
            status = request.POST.get('status', 'Pending')
            
            # Handle dates
            start_date = None
            start_date_str = request.POST.get('start_date', '')
            if start_date_str and start_date_str.strip():
                try:
                    start_date = start_date_str
                except:
                    pass
            
            expected_end_date = None
            expected_end_date_str = request.POST.get('expected_end_date', '')
            if expected_end_date_str and expected_end_date_str.strip():
                try:
                    expected_end_date = expected_end_date_str
                except:
                    pass
            
            actual_start_date = None
            actual_start_date_str = request.POST.get('actual_start_date', '')
            if actual_start_date_str and actual_start_date_str.strip():
                try:
                    actual_start_date = actual_start_date_str
                except:
                    pass
            
            # Handle file uploads
            site_photo_1 = request.FILES.get('site_photo_1')
            site_photo_2 = request.FILES.get('site_photo_2')
            site_photo_3 = request.FILES.get('site_photo_3')
            commencement_certificate_document = request.FILES.get('commencement_certificate_document')
            supervisor_report_document = request.FILES.get('supervisor_report_document')
            other_document = request.FILES.get('other_document')
            
            if is_edit:
                # Update existing record
                work_start.start_date = start_date
                work_start.expected_end_date = expected_end_date
                work_start.actual_start_date = actual_start_date
                work_start.site_location = site_location
                work_start.supervisor_name = supervisor_name
                work_start.contractor_name = contractor_name
                work_start.initial_work_status = initial_work_status
                work_start.remarks = remarks
                work_start.status = status
                work_start.updated_at = timezone.now()
                
                # Update documents
                if site_photo_1:
                    work_start.site_photo_1 = site_photo_1
                if site_photo_2:
                    work_start.site_photo_2 = site_photo_2
                if site_photo_3:
                    work_start.site_photo_3 = site_photo_3
                if commencement_certificate_document:
                    work_start.commencement_certificate_document = commencement_certificate_document
                if supervisor_report_document:
                    work_start.supervisor_report_document = supervisor_report_document
                if other_document:
                    work_start.other_document = other_document
                    
                work_start.save()
                
                messages.success(request, "काम सुरू माहिती यशस्वीरित्या अद्यतनित केली")
            else:
                # Create new record
                work_start = Work_Start.objects.create(
                    work_master=work_master,
                    start_date=start_date,
                    expected_end_date=expected_end_date,
                    actual_start_date=actual_start_date,
                    site_location=site_location,
                    supervisor_name=supervisor_name,
                    contractor_name=contractor_name,
                    initial_work_status=initial_work_status,
                    remarks=remarks,
                    status=status,
                    site_photo_1=site_photo_1,
                    site_photo_2=site_photo_2,
                    site_photo_3=site_photo_3,
                    commencement_certificate_document=commencement_certificate_document,
                    supervisor_report_document=supervisor_report_document,
                    other_document=other_document,
                    started_by=kosh_user
                )
                
                messages.success(request, "काम सुरू माहिती यशस्वीरित्या जतन केली")
            
            # Update Work Master status
            if status == 'Started':
                work_master.work_start_completed = True
                work_master.work_start_completed_date = timezone.now()
                work_master.work_start_status = 'Started'
                work_master.work_start_date = actual_start_date or start_date
                work_master.save()
            elif status == 'On Hold':
                work_master.work_start_status = 'On Hold'
                work_master.save()
            
            return redirect('Activity-Work-Start', work_id=work_id)
            
        except Exception as e:
            messages.error(request, f"एरर आली: {str(e)}")

    context = {
        'user_type': 'Kosh',
        'kosh_user': kosh_user,
        'work_master': work_master,
        'work_start': work_start,
        'is_edit': is_edit,
        'load_sidebar': "load_sidebar",
    }

    return render(request, 'Activity-Work-Start.html', context)

